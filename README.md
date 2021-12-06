## Git Repository 소개

안녕하세요.

해당 Git Repositry는 웹 사이트 [Zara](https://www.zara.com/kr/)를 모티브로 한 프로젝트를 진행할 예정입니다.

보다 다양성이 많은 여성 옷에 대해서만 구현할 예정입니다.

최초 초안 기획부터 구현까지 혼자했으며, EC2나 RDS까지 배포는 비용 문제상 하지 않을 생각입니다.

프로젝트 기간은 12월 4일(토) ~ 12월 18일(토)까지 입니다.

<br>

## Contents

1. Skill & Tools
2. ERD Diagram
3. EndPoint
4. 구현 사항 상세 설명
5. Unit Test 결과
6. Commit Message GuideLines
7. Reference

<br>

## Skill & Tools
* BackEnd : Python, django, django-environ, bcrypt, jwt, Faker
* DataBase : sqlite3
* ETC Tool : Git, GitHub, Postman

<br>

## ERD Diagram

![zara](https://user-images.githubusercontent.com/88086271/144640885-edc5a3d4-cf7f-49e7-9b98-28873329471e.png)


<br>

## EndPoint

1. 회원가입

POST /users/signup

<br>

## 구현 사항 상세 설명

1. 회원가입

BODY : email, password, role_id

이메일과 비밀번호를 받아서 회원가입을 진행합니다.

그리고 role_id를 통해 얻은 등급을 통하여, 유저/관리자에 맞게 회원정보를 저장합니다.

3개의 변수가 요청으로 오지 않거나, 3개의 요청이 왔는데 KEY값이 다를 경우 KEY ERROR를 발생시킵니다.

이미 회원가입된 메일이 있을 경우, Integrity Error를 발생시키며

role_id가 roles 테이블에 존재하지 않는 경우 Role.DoesNotExist가 발생합니다.

구현 사항에 대한 상세 코드 : [클릭](https://velog.io/@kyleee/1.-%ED%98%BC%EC%9E%90-%EB%A7%8C%EB%93%A4%EC%96%B4%EB%B3%B4%EB%8A%94-Zara-%ED%9A%8C%EC%9B%90%EA%B0%80%EC%9E%85)

<br>

## Unit Test 결과

<br>

## Commit Message GuideLines

1. 분류는 Add / Remove / Modify / Fix / Refactor / Docs로 나뉜다.
2. ADD : 기능 추가할 시 기입
3. Remove : 폴더/파일 삭제할 시 기입
4. Modify : 수정 (JSON 데이터 포맷 등 코드가 아닌 사항을 변경할 시 기입)
5. Fix : 버그/오류 해결할 시 기입
6. Refactor : 코드 리팩토링 (ORM구문 변경, 불필요 코드 제거, 성능 개선 등 코드 관련된 내용 수정할 시 기입)
7. Docs : 문서에 관련된 수정작업(README 등)

<br>

## Reference
* 이 프로젝트는 [Zara](https://www.zara.com/kr/) 웹 사이트를 참조하여 학습 목적으로 만들었습니다.
* 실무 수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우, 법적으로 문제가 있을 수 있습니다.
