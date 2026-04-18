google_login_request_example = {
    "token": "ya29.a0AfH6SMA...example-google-token",
}

google_login_response_example = {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "name": "User Example",
        "first_name": "User",
        "last_name": "Example",
    },
}

create_record_request_example = {
    "patient_full_name": "María Pérez",
    "patient_identifier": "HC-123456",
    "clinical_reference": "Fractura distal de radio",
    "study_date": "2026-04-18",
    "image_url": "https://res.cloudinary.com/demo/image/upload/v168.../radiografia.jpg",
    "image_public_id": "radiografia_abc123",
}

update_record_request_example = {
    "clinical_reference": "Seguimiento de fractura distal de radio",
    "study_date": "2026-04-20",
}

record_response_example = {
    "id": 1,
    "patient_full_name": "María Pérez",
    "patient_identifier": "HC-123456",
    "clinical_reference": "Fractura distal de radio",
    "study_date": "2026-04-18",
    "image_url": "https://res.cloudinary.com/demo/image/upload/v168.../radiografia.jpg",
    "image_public_id": "radiografia_abc123",
    "created_by": 1,
    "created_at": "2026-04-18T12:00:00Z",
    "updated_at": "2026-04-18T12:00:00Z",
}

pagination_query_example = {
    "page": 1,
    "page_size": 20,
    "patient_full_name": "María",
    "patient_identifier": "HC-123456",
    "study_date": "2026-04-18",
    "order_by": "-study_date",
}
