import uvicorn

if __name__ == "__main__":
    #  config = uvicorn.Config("app.app:app", port=5000, log_level="info", reload=True)
    # server = uvicorn.Server(config)
    # server.run() ## with server object app reload doesn't work.
    uvicorn.run("app.app:app", port=5000, log_level="info", reload=True)