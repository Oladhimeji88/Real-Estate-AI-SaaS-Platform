from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI(title="Notifications Service", version="0.1.0")
connections: list[WebSocket] = []

@app.websocket('/ws/alerts')
async def ws_alerts(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            message = await websocket.receive_text()
            for conn in connections:
                await conn.send_text(f"alert:{message}")
    except WebSocketDisconnect:
        connections.remove(websocket)

@app.post('/api/notifications/webhook')
def webhook_event(payload: dict):
    return {"received": True, "event": payload}

@app.get('/health')
def health():
    return {"status": "ok", "service": "notifications"}
