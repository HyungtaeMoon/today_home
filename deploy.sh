#!/usr/bin/env bash

# requirements.txt 를 생성
pipenv lock --requirements > requirements.txt

# 수정한 내용 반영
git add -A

# secrets 디렉토리, requirements.txt를 staging 상태로 변환
git add -f .secrets/ requirements.txt

# staged 상태로 eb 배포
eb deploy --profile eb-today-home --staged

# git에서 secrets, requirements.txt 를 reset
git reset HEAD .secrets/ requirements.txt

# requirements.txt 삭제
rm requirements.txt
