import uvicorn
uvicorn.run("chat_endpoint:app", host="0.0.0.0", port=8001, reload=False, log_level="debug")
