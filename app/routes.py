from app.models import Project, Contributor, db  
from app import app
from flask import request, jsonify


@app.route('/create_or_get_project', methods=['POST'])
def create_or_get_project():
    project_data = request.json

    project_title = project_data.get('project_title')
    
    existing_project = Project.query.filter_by(project_title=project_title).first()
    if existing_project:
        project_data["id"] = existing_project.id  # Preserve existing ID
        return jsonify(message="Project already exists", project_data=project_data)
    
    new_project = Project(**project_data)
    db.session.add(new_project)
    db.session.commit()
    
    return jsonify(message="Project created successfully", project_data=project_data)


@app.route('/contribute', methods=['POST'])
def contribute():
    contributor_address = request.json.get('contributor_address')
    project_title = request.json.get('project_title')
    contribution_amount = float(request.json.get('contribution_amount'))

    contributor = Contributor(
        contributor_address=contributor_address,
        project_title=project_title,
        contribution=contribution_amount
    )
    contributor.save()

    project = Project.query.filter_by(project_title=project_title).first()
    project.total_contributors += 1
    project.total_contribution += contribution_amount
    db.session.commit()

    if project.total_contribution >= project.project_target:
        pass
        # Handle the case where the target is reached

    return jsonify(message="Contribution successful")



@app.route('/get_all_projects', methods=['GET'])
def get_all_projects():
    projects = Project.query.all()

    project_list = []
    for project in projects:
        project_data = {
            "id": project.id,
            "address": project.address,
            "nickname": project.nickname,
            "project_title": project.project_title,
            "project_description": project.project_description,
            "project_category": project.project_category,
            "project_target": project.project_target,
            "minimum_buy_in": project.minimum_buy_in,
            "roi": project.roi,
            "stake_amount": project.stake_amount,
            "photo": project.photo,
            "total_contributors": project.total_contributors,
            "total_contribution": project.total_contribution
        }
        project_list.append(project_data)

    return jsonify(projects=project_list)


@app.route('/filter_contributions_by_project_title', methods=['GET'])
def filter_contributions_by_project_title():
    project_title = request.args.get('project_title')
    
    contributions = Contributor.query.filter_by(project_title=project_title).all()
    
    contribution_list = []
    for contribution in contributions:
        contribution_data = {
            "id": contribution.id,
            "contributor_address": contribution.contributor_address,
            "project_title": contribution.project_title,
            "contribution": contribution.contribution,
        }
        contribution_list.append(contribution_data)
    
    return jsonify(contributions=contribution_list)



@app.route('/get_contributed_project_addresses', methods=['GET'])
def get_contributed_project_addresses():
    contributor_address = request.args.get('contributor_address')
    
    contributions = Contributor.query.filter_by(contributor_address=contributor_address).all()
    
    project_addresses = [contribution.project_address for contribution in contributions]
    
    return jsonify(project_addresses=project_addresses)




@app.route('/get_contributed_projects', methods=['GET'])
def get_contributed_projects():
    contributor_address = request.args.get('contributor_address')
    
    contributions = Contributor.query.filter_by(contributor_address=contributor_address).all()
    
    contributed_projects = []
    for contribution in contributions:
        project = Project.query.filter_by(project_title=contribution.project_title).first()
        if project:
            project_data = {
                "id": project.id,
                "address": project.address,
                "nickname": project.nickname,
                "project_title": project.project_title,
                "project_description": project.project_description,
                "project_category": project.project_category,
                "project_target": project.project_target,
                "minimum_buy_in": project.minimum_buy_in,
                "roi": project.roi,
                "stake_amount": project.stake_amount,
                "photo": project.photo,
                "total_contributors": project.total_contributors,
                "total_contribution": project.total_contribution
            }
            contributed_projects.append(project_data)
    
    return jsonify(contributed_projects=contributed_projects)


# Filter all projects created by a particular user.
@app.route('/filter_projects_by_address', methods=['GET'])
def filter_projects_by_address():
    address = request.args.get('address')
    
    projects = Project.query.filter_by(address=address).all()
    
    project_list = []
    for project in projects:
        project_data = {
            "id": project.id,
            "address": project.address,
            "nickname": project.nickname,
            "project_title": project.project_title,
            "project_description": project.project_description,
            "project_category": project.project_category,
            "project_target": project.project_target,
            "minimum_buy_in": project.minimum_buy_in,
            "roi": project.roi,
            "stake_amount": project.stake_amount,
            "photo": project.photo,
            "total_contributors": project.total_contributors,
            "total_contribution": project.total_contribution
        }
        project_list.append(project_data)
    
    return jsonify(projects=project_list)


@app.route('/filter_projects_by_title', methods=['GET'])
def filter_projects_by_title():
    project_title = request.args.get('project_title')
    
    project = Project.query.filter_by(project_title=project_title).first()
    if not project:
        return jsonify(message="Project not found"), 404
    
    project_data = {
        "id": project.id,
        "address": project.address,
        "nickname": project.nickname,
        "project_title": project.project_title,
        "project_description": project.project_description,
        "project_category": project.project_category,
        "project_target": project.project_target,
        "minimum_buy_in": project.minimum_buy_in,
        "roi": project.roi,
        "stake_amount": project.stake_amount,
        "photo": project.photo,
        "total_contributors": project.total_contributors,
        "total_contribution": project.total_contribution
    }
    
    return jsonify(project_data)


@app.route('/delete_project', methods=['DELETE'])
def delete_project():
    project_title = request.json.get('project_title')
    
    project = Project.query.filter_by(project_title=project_title).first()
    if not project:
        return jsonify(message="Project not found"), 404
    
    if project.total_contributors == 0 and project.total_contribution == 0:
        db.session.delete(project)
        db.session.commit()
        return jsonify(message="Project deleted successfully")
    else:
        return jsonify(message="Project has ongoing contributions and cannot be deleted"), 400





@app.route('/update_project', methods=['PUT'])
def update_project():
    project_data = request.json
    project_title = project_data.get('project_title')

    project = Project.query.filter_by(project_title=project_title).first()
    if not project:
        return jsonify(message="Project not found"), 404
    
    # List of immutable fields
    immutable_fields = ["id", "address", "total_contributors", "total_contribution"]
    
    # Check for any provided fields to update
    fields_to_update = {key: value for key, value in project_data.items() if key not in immutable_fields}
    
    if not fields_to_update:
        return jsonify(message="No fields provided to update"), 400
    
    for field, value in fields_to_update.items():
        setattr(project, field, value)
    
    db.session.commit()
    
    return jsonify(message="Project updated successfully", updated_fields=list(fields_to_update.keys()))



@app.route('/transfer_ownership', methods=['PUT'])
def transfer_ownership():
    transfer_data = request.json
    project_title = transfer_data.get('project_title')
    new_address = transfer_data.get('new_address')

    project = Project.query.filter_by(project_title=project_title).first()
    if not project:
        return jsonify(message="Project not found"), 404
    
    project.address = new_address
    db.session.commit()
    
    return jsonify(message="Ownership transferred successfully")
