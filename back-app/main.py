# fastapi-app/main.py

from fastapi import FastAPI, HTTPException
import mysql.connector
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import subprocess

app = FastAPI()

# AWS RDS 서버에 연결
conn = mysql.connector.connect(
    host="api-database.c98wk66a2xnf.ap-northeast-1.rds.amazonaws.com",
    user="root",
    password="test1234",
    database="api"
)
cursor = conn.cursor()

# 데이터를 전송하기 위한 모델 정의
class TestData(BaseModel):
    target_url: str
    test_name: str
    user_num: int
    user_plus_num: int
    interval_time: int
    plus_count: int

def run_load_testing_script(url, initial_user_count, additional_user_count, interval_time, repeat_count, test_id):
    command = [
        "python",
        "runner.py",
        "--url", url,
        "--initial_user_count", str(initial_user_count),
        "--additional_user_count", str(additional_user_count),
        "--interval_time", str(interval_time),
        "--repeat_count", str(repeat_count),
        "--test_id", str(test_id)
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# 테스트 목록 불러오기
@app.get('/testcase')
async def read_list():
    try:
        cursor.execute("SELECT test_id, test_name FROM test")
        result = cursor.fetchall()
        test_data = [{"test_id": row[0], "test_name": row[1]} for row in result]
        return {"testData": test_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# 테스트 생성
@app.post('/testcase')
async def create_test(data: TestData):
    try:
        cursor.execute(
            """
            INSERT INTO test (target_url, test_name, user_num, user_plus_num, interval_time, plus_count)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (data.target_url, data.test_name, data.user_num, data.user_plus_num, data.interval_time, data.plus_count)
        )
        conn.commit()
        test_id = cursor.lastrowid
        return {"test_id": test_id, "test_name": data.test_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# 테스트 삭제
@app.delete("/testcase/{test_id}")
async def delete_test(test_id: int):
    try:
        cursor.execute("DELETE FROM test WHERE test_id = %s", (test_id,))
        conn.commit()
        return {"message": "Test deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/testcase/{test_id}/execute/")
async def execute_test(test_id: int):
    try:
        cursor.execute("SELECT * FROM test WHERE test_id = %s", (test_id,))
        test_data = cursor.fetchone()
        if test_data:
            test_id, target_url, test_name, user_num, user_plus_num, interval_time, plus_count = test_data
            run_load_testing_script(target_url, user_num, user_plus_num, interval_time, plus_count, test_id)
            return {
                "test_id": test_id,
                "target_url": target_url,
                "test_name": test_name,
                "user_num": user_num,
                "user_plus_num": user_plus_num,
                "interval_time": interval_time,
                "plus_count": plus_count,
            }
        else:
            raise HTTPException(status_code=404, detail="Testcase not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


