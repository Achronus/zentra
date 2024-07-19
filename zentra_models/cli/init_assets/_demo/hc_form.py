from zentra_models.form import Form, FormSection
from zentra_models.form.fields import (
    TextField,
    EmailField,
    PhoneField,
    DateField,
    RadioGroupField,
    TextareaField,
    CheckboxField,
    SelectField,
    FileUploadField,
)


personal_info = FormSection(
    title="Personal Information",
    desc=None,
    fields=[
        TextField(
            id="name",
            label="Full Name",
            placeholder="ex: Adam",
            icon=False,
        ),
        [
            EmailField(
                id="email",
                label="Email Address",
                placeholder="ex: johndoe@youremail.com",
                icon=True,
            ),
            PhoneField(
                id="phone",
                label="Phone Number",
                placeholder=None,
                country="GB",
            ),
        ],
        [
            DateField(
                id="dob",
                label="Date Of Birth",
                placeholder="Select your birth date",
                icon=True,
            ),
            RadioGroupField(
                id="gender",
                label="Gender",
                options=["male", "female", "other"],
            ),
        ],
        [
            TextField(
                id="address",
                label="Address",
                placeholder="ex: 14 New Road, Cambridge, UK",
                icon=False,
            ),
            TextField(
                id="occupation",
                label="Occupation",
                placeholder="ex: Software Engineer",
                icon=False,
            ),
        ],
        [
            TextField(
                id="emergencyContactName",
                label="Emergency Contact Name",
                placeholder="Guardian's name",
                icon=False,
            ),
            PhoneField(
                id="emergencyContactNumber",
                label="Emergency Contact Number",
                placeholder=None,
                country="GB",
            ),
        ],
    ],
)

medical_info = FormSection(
    title="Medical Information",
    desc=None,
    fields=[
        SelectField(
            id="physician",
            label="Primary Physician",
            placeholder="Select a physician",
            items=[],
            icon=False,
        ),
        [
            TextField(
                id="insuranceProvider",
                label="Insurance Provider",
                placeholder="ex: Axa",
                icon=False,
            ),
            TextField(
                id="insurancePolicyNumber",
                label="Insurance Policy Number",
                placeholder="ex: ABC123",
                icon=False,
            ),
        ],
        [
            TextareaField(
                id="allergies",
                label="Allergies (if any)",
                placeholder="ex: Peanuts, Penicillin, Pollen",
                icon=False,
            ),
            TextareaField(
                id="medication",
                label="Current Medications",
                placeholder="ex: Ibuprofen 200mg, Levothyroxine 50mcg",
                icon=False,
            ),
        ],
        [
            TextareaField(
                id="familyMedicalHistory",
                label="Family Medical History (if relevant)",
                placeholder="ex: Mother had breast cancer",
                icon=False,
            ),
            TextareaField(
                id="pastMedicalHistory",
                label="Past Medical History",
                placeholder="ex: ASthma diagnosis in childhood",
                icon=False,
            ),
        ],
    ],
)

id_section = FormSection(
    title="Identification and Verification",
    desc=None,
    fields=[
        SelectField(
            id="idType",
            label="Identification Type",
            placeholder="Select an option",
            items=[],
            icon=False,
        ),
        TextField(
            id="idNumber",
            label="Identification Number",
            placeholder="ex: 123456",
            icon=False,
        ),
        FileUploadField(
            id="idDocuments",
            label="Scanned Copy of Identification Document",
            file_types=["SVG", "PNG", "JPG", "PDF"],
            max_img_size="800x400",
            max_file_size="20MB",
            multiple=False,
        ),
    ],
)

consent_section = FormSection(
    title="Consent and Privacy",
    desc=None,
    fields=[
        CheckboxField(
            id="treatmentConsent",
            label="I consent to receive treatment for my health condition.",
        ),
        CheckboxField(
            id="disclosureConsent",
            label="I consent to the use and disclosure of my health information for treatment purposes.",
        ),
        CheckboxField(
            id="privacyConsent",
            label="I acknowledge that I have reviewed and agree to the privacy policy.",
        ),
    ],
)

form = Form(
    name="HealthcareForm",
    title="Getting Setup",
    desc="Let us know more about you!",
    sections=[
        personal_info,
        medical_info,
        id_section,
        consent_section,
    ],
    btn_text="Submit and Continue",
)
