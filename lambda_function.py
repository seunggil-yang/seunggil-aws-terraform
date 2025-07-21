import json
import os
import boto3

# PyMySQL을 조건부로 import
try:
    import pymysql
    PYMYSQL_AVAILABLE = True
except ImportError:
    PYMYSQL_AVAILABLE = False
    print("PyMySQL not available, using mock data")

def lambda_handler(event, context):
    try:
        # 환경 변수에서 설정값 가져오기
        mysql_host = os.environ['MYSQL_HOST']
        mysql_password = os.environ['MYSQL_PASSWORD']
        region = os.environ.get('REGION', 'us-east-1')

        # team_member 데이터 조회
        if PYMYSQL_AVAILABLE:
            # MySQL 연결
            connection = pymysql.connect(
                host=mysql_host,
                port=3306,
                user='root',
                password=mysql_password,
                database='team_practice_db'
            )

            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute("SELECT * FROM team_member ORDER BY id")
                team_members = cursor.fetchall()

            connection.close()
        else:
            # PyMySQL이 없으면 하드코딩된 데이터 사용
            team_members = [
                {"id": 1, "name": "Jaehong Yang", "role": "Service Platform Lead"},
                {"id": 2, "name": "Dongbeom Kim", "role": "Backend"},
                {"id": 3, "name": "Hyeyoung Lee", "role": "QA / Infra"},
                {"id": 4, "name": "Seunggil Yang", "role": "Infra / DevOps"},
                {"id": 5, "name": "Yoonki Cho", "role": "Frontend"},
                {"id": 6, "name": "Gookseong Kim", "role": "Frontend / Backend"},
                {"id": 7, "name": "Jerry", "role": "Data Engineering"},
                {"id": 8, "name": "Aiden", "role": "Backend"}
            ]

        # EC2 정보 조회
        ec2_client = boto3.client('ec2', region_name=region)

        # t4g.nano 인스턴스만 조회
        response = ec2_client.describe_instances(
            Filters=[
                {
                    'Name': 'instance-type',
                    'Values': ['t4g.nano']
                },
                {
                    'Name': 'instance-state-name',
                    'Values': ['running', 'stopped', 'pending', 'stopping']
                }
            ]
        )

        # 인스턴스 정보 추출
        aws_instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                aws_instances.append({
                    'instance_id': instance['InstanceId'],
                    'instance_type': instance['InstanceType'],
                    'state': instance['State']['Name'],
                    'private_ip': instance.get('PrivateIpAddress', 'N/A')
                })

        # 응답 데이터 구성
        response_data = {
            'data': {
                'aws_instances': aws_instances,
                'region': region,
                'team_members': team_members,
                'mysql_connection': 'real' if PYMYSQL_AVAILABLE else 'mock'
            },
            'status': 'success'
        }

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response_data, indent=2)
        }

    except Exception as e:
        error_response = {
            'data': {
                'error': str(e),
                'mysql_available': PYMYSQL_AVAILABLE
            },
            'status': 'error'
        }

        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(error_response, indent=2)
        }