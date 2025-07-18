#!/bin/bash

# 시스템 업데이트
yum update -y

# Docker 설치
yum install -y docker
systemctl start docker
systemctl enable docker

# ec2-user를 docker 그룹에 추가
usermod -a -G docker ec2-user

# MySQL 8.0 Docker 컨테이너 실행 (ARM64 지원)
docker run -d \
  --name mysql-container \
  --restart unless-stopped \
  -e MYSQL_ROOT_PASSWORD="${mysql_password}" \
  -e MYSQL_DATABASE=team_practice_db \
  -p 3306:3306 \
  mysql:8.0

# MySQL이 시작될 때까지 대기
sleep 30

# 데이터베이스 테이블 생성 및 데이터 입력
docker exec mysql-container mysql -uroot -p"${mysql_password}" team_practice_db -e "
CREATE TABLE team_member (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    role VARCHAR(100)
);

INSERT INTO team_member VALUES
(1, 'Jaehong Yang', 'Service Platform Lead'),
(2, 'Dongbeom Kim', 'Backend'),
(3, 'Hyeyoung Lee', 'QA / Infra'),
(4, 'Seunggil Yang', 'Infra / DevOps'),
(5, 'Yoonki Cho', 'Frontend'),
(6, 'Gookseong Kim', 'Frontend / Backend'),
(7, 'Jerry', 'Data Engineering'),
(8, 'Aiden', 'Backend');
"

# 설치 완료 로그
echo "MySQL Docker setup completed at $(date)" >> /var/log/user-data.log