from requests import get, post, delete


print(get('http://localhost:5000/api/jobs').json())
print(get('http://localhost:5000/api/jobs/1').json())
print(get('http://localhost:5000/api/jobs/586').json())
print(get('http://localhost:5000/api/jobs/weret').json())

print(post('http://localhost:5000/api/jobs',
            json={
                'team_leader': 3,
                'job': "Проект по вебу",
                'work_size': 42,
                'is_finished': True

            }).json())
