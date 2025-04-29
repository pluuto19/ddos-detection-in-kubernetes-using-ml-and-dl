from fastapi import FastAPI, Request
import hashlib
import os
import uvicorn
import time

app = FastAPI()

CPU_INTENSITY = int(os.getenv("CPU_INTENSITY", "100000")) # number of hashing iterations
MEMORY_SIZE = int(os.getenv("MEMORY_SIZE", "50"))

@app.post("/process")
async def process_data(request: Request):
    start_time = time.time()
    
    body = await request.body()
    data = body.decode("utf-8")
    
    memory_chunk = ["X" * 1024 * 1024 for _ in range(MEMORY_SIZE)]
    
    result = data
    for i in range(CPU_INTENSITY):
        result = hashlib.sha512(result.encode()).hexdigest()
    
    del memory_chunk
    
    return {
        "hash_result": result[:32]
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    port = int(os.getenv("HTTP_PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)