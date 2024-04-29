import flask
from flask import jsonify, make_response, request
import json

from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()

    return json.dumps(
        {
            'jobs': 
            [item.to_dict(only=('size', 'user.name', 'user.surname', 'is_finished'))
            for item in jobs]
        }, ensure_ascii=False, indent=3
    )



@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_job(jobs_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(jobs_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)

    return json.dumps(
        {
            'jobs': job.to_dict(only=('size', 'user.name', 'user.surname', 'is_finished'))
        }, ensure_ascii=False
    )

@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                ['team_leader', 'namep', 'size', 'boost', 'biograph', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    job = Jobs(
        team_leader=request.json['team_leader'],
        namep=request.json['namep'],
        size=request.json['size'],
        boost=request.json['boost'],
        biograph=request.json['biograph'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(job)
    db_sess.commit()
    return jsonify({'id': job.id})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_jobs(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})

    