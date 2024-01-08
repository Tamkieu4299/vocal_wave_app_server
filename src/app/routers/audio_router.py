import os
import uuid
import requests
import datetime
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
from io import BytesIO
from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, status, Form
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from ..crud.audio_crud import (
    all_audios,
    create_audio,
    read_audio,
    soft_delete,
    update_audio,
    search_audios_by_name,
    audios_by_emotion
)
from ..db.database import get_db
from ..models.audio_model import Audio
from ..schemas.playlist_audio_schema import (
    AudioBaseSchema,
    AudioSchema,
    AudioUpdate,
    AudioResponseSchema,
    CreateAudioSchema,
)
from ..utils.exception import InvalidFileType, NotFoundException
from ..utils.handle_file import save_to_FS, validate_file_type, get_audio_file_extension
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()

@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=AudioResponseSchema,
)
async def add_audio(
    audio_data: CreateAudioSchema = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Create an audio"""
    is_audio = validate_file_type(file, "audio")
    
    # # Check if not an audio
    if is_audio is False:
        raise InvalidFileType(detail="Your upload file must be an audio")

    extension = get_audio_file_extension(file)
    file_content = await file.read()

    audio = AudioSegment.from_file(BytesIO(file_content))
    duration_seconds = len(audio) / 1000
    
    data = audio_data.dict()
    data["durations"] = duration_seconds
    data["emotion_type"] = data["emotion_type"].lower()
    audio: Audio = Audio(**data)
    new_audio = create_audio(audio, db)
    
    # output_file = f"./static/audio/{audio_data.audio_name}.wav"
    save_to_FS("audio", audio_data.audio_name, "mp3", file_content)
    # output_audio.export(output_file, format="wav")
    

    # Add metada
    logger.info(
        f"Created audio name {new_audio.audio_name} with ID {new_audio.audio_id}"
    )

    return new_audio.__dict__


@router.post("/soft-delete/{audio_id}", response_model=AudioSchema)
async def soft_delete_by_id(audio_id: str, db: Session = Depends(get_db)):
    """Get the audio by its id"""
    audio = soft_delete(audio_id, db)

    if audio is None:
        logger.info(f"Invalid audio with ID: {audio_id}")
        raise NotFoundException(detail=f"Invalid audio with ID: {audio_id}")
    logger.info(f"Soft delete audio with ID: {audio_id}")
    return audio.__dict__


@router.get("/get/{audio_id}", response_model=AudioSchema)
async def get_audio_by_id(audio_id: str, db: Session = Depends(get_db)):
    """Get the audio by its id"""
    audio = read_audio(audio_id, db)
    if audio is None:
        logger.info(f"Invalid audio with ID: {audio_id}")
        raise NotFoundException(detail=f"Invalid audio with ID: {audio_id}")

    logger.info(f"Get audio with ID: {audio.audio_id}")
    return audio.__dict__


@router.put("/update/{id}", response_model=AudioBaseSchema)
async def update_audio_by_id(
    id: str, audio: AudioUpdate, db: Session = Depends(get_db)
):
    """Update the video following its id"""
    updated_audio = update_audio(id, audio, db)
    if updated_audio is None:
        logger.info(f"Invalid audio with ID: {id}")
        raise NotFoundException(detail=f"Invalid audio with ID: {id}")

    logger.info(f"Updated audio with ID: {id}")
    return updated_audio.__dict__


@router.get("/search/", response_model=List[AudioResponseSchema])
async def get_audios(db: Session = Depends(get_db)):
    audios = await all_audios(db)
    audios_dict_list = [i.__dict__ for i in audios]
    logger.info(f"Number of audios: {len(audios)}")
    return audios_dict_list


@router.get("/search_emotion")
async def search_audios(db: Session = Depends(get_db)):
    #Call ML method
    response = requests.get("http://host.docker.internal:8002/face_recognition")
    # emotion = "happy"
    if response.status_code == 200:
        return response.json()
    return 'happy'
    # if response.status_code == 200:
    #     emotion = response.json()
    # audios = await audios_by_emotion(emotion, db)
    # audios_dict_list = [i.__dict__ for i in audios]
    # logger.info(f"Number of audios: {len(audios)}")
    # return audios_dict_list


@router.get("/search/{emotion}", response_model=List[AudioResponseSchema])
async def get_audios_by_emotion(emotion: str, db: Session = Depends(get_db)):
    audios = await audios_by_emotion(emotion, db)
    audios_dict_list = [i.__dict__ for i in audios]
    logger.info(f"Number of audios: {len(audios)}")
    return audios_dict_list
