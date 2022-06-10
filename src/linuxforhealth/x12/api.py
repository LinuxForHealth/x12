from fastapi import FastAPI, Header, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import uvicorn
from typing import Dict, Optional, List
from linuxforhealth.x12.config import get_x12_api_config, X12ApiConfig
from linuxforhealth.x12.io import X12SegmentReader, X12ModelReader
from linuxforhealth.x12.parsing import X12ParseException
from pydantic import ValidationError, BaseModel, Field

app = FastAPI()


@app.exception_handler(RequestValidationError)
async def request_validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {"detail": "Invalid request. Expected {'x12': <x12 message string>}"}
        ),
    )


class X12Request(BaseModel):
    """
    The X12 Request object
    """

    x12: str = Field(description="The X12 payload to process, conveyed as a string")

    class Config:
        schema_extra = {
            "example": {
                "x12": "ISA*03*9876543210*01*9876543210*30*000000005      *30*12345          *131031*1147*^*00501*000000907*1*T*:~GS*HS*000000005*54321*20131031*1147*1*X*005010X279A1~ST*270*1234*005010X279A1~BHT*0022*13*10001234*20060501*1319~HL*1**20*1~NM1*PR*2*ABC COMPANY*****PI*842610001~HL*2*1*21*1~NM1*1P*2*BONE AND JOINT CLINIC*****SV*2000035~HL*3*2*22*0~TRN*1*93175-012547*9877281234~NM1*IL*1*SMITH*ROBERT****MI*11122333301~DMG*D8*19430519~DTP*291*D8*20060501~EQ*30~SE*13*1234~GE*1*1~IEA*1*000000907~",
            }
        }


@app.post("/x12")
async def post_x12(
    x12_request: X12Request,
    lfh_x12_response: Optional[str] = Header(default="models"),
) -> List[Dict]:
    """
    Processes an incoming X12 payload.

    Requests are submitted as:

    {
       "x12": <x12 message string>
    }

    The response payload is a JSON document containing either the "raw" X12 segments, or a rich
    X12 domain model. The response type defaults to the domain model and is configured using the
    LFH-X12-RESPONSE header. Valid values include: "segments" or "models".

    :param x12_request: The X12 request model/object.
    :param lfh_x12_response: A header value used to drive processing.

    :return: The X12 response - List[List] (segments) or List[Dict] (models)
    """
    if lfh_x12_response.lower() not in ("models", "segments"):
        lfh_x12_response = "models"

    try:
        if lfh_x12_response.lower() == "models":
            with X12ModelReader(x12_request.x12) as r:
                api_results = [m.dict() for m in r.models()]
        else:
            with X12SegmentReader(x12_request.x12) as r:
                api_results = []
                for segment_name, segment in r.segments():
                    segment_data = {
                        f"{segment_name}{str(i).zfill(2)}": v
                        for i, v in enumerate(segment)
                    }
                    api_results.append(segment_data)

    except (X12ParseException, ValidationError) as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid X12 payload. To troubleshoot please run the LFH X12 CLI",
        )
    else:
        return api_results


def run_server():
    """Launches the API server"""
    config: X12ApiConfig = get_x12_api_config()

    uvicorn_params = {
        "app": config.x12_uvicorn_app,
        "host": config.x12_uvicorn_host,
        "port": config.x12_uvicorn_port,
        "reload": config.x12_uvicorn_reload,
    }

    uvicorn.run(**uvicorn_params)


if __name__ == "__main__":
    run_server()
