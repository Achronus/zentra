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
            name="name",
            label="Full Name",
            placeholder="ex: Adam",
        ),
        [
            EmailField(
                name="email",
                label="Email Address",
                placeholder="ex: johndoe@youremail.com",
                icon=True,
            ),
            PhoneField(
                name="phone",
                label="Phone Number",
                country="GB",
            ),
        ],
        [
            DateField(
                name="dob",
                label="Date Of Birth",
                placeholder="Select your birth date",
                icon=True,
            ),
            RadioGroupField(
                name="gender",
                label="Gender",
                options=["male", "female", "other"],
            ),
        ],
        [
            TextField(
                name="address",
                label="Address",
                placeholder="ex: 14 New Road, Cambridge, UK",
                icon=False,
            ),
            TextField(
                name="occupation",
                label="Occupation",
                placeholder="ex: Software Engineer",
                icon=False,
            ),
        ],
        [
            TextField(
                name="emergencyContactName",
                label="Emergency Contact Name",
                placeholder="Guardian's name",
                icon=False,
            ),
            PhoneField(
                name="emergencyContactNumber",
                label="Emergency Contact Number",
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
            name="physician",
            label="Primary Physician",
            placeholder="Select a physician",
            api_url="api",
        ),
        [
            TextField(
                name="insuranceProvider",
                label="Insurance Provider",
                placeholder="ex: Axa",
            ),
            TextField(
                name="insurancePolicyNumber",
                label="Insurance Policy Number",
                placeholder="ex: ABC123",
            ),
        ],
        [
            TextareaField(
                name="allergies",
                label="Allergies (if any)",
                placeholder="ex: Peanuts, Penicillin, Pollen",
            ),
            TextareaField(
                name="medication",
                label="Current Medications",
                placeholder="ex: Ibuprofen 200mg, Levothyroxine 50mcg",
            ),
        ],
        [
            TextareaField(
                name="familyMedicalHistory",
                label="Family Medical History (if relevant)",
                placeholder="ex: Mother had breast cancer",
            ),
            TextareaField(
                name="pastMedicalHistory",
                label="Past Medical History",
                placeholder="ex: ASthma diagnosis in childhood",
            ),
        ],
    ],
)

id_section = FormSection(
    title="Identification and Verification",
    desc=None,
    fields=[
        SelectField(
            name="idType",
            label="Identification Type",
            placeholder="Select an option",
            items=[],
            icon=False,
        ),
        TextField(
            name="idNumber",
            label="Identification Number",
            placeholder="ex: 123456",
            icon=False,
        ),
        FileUploadField(
            name="idDocuments",
            label="Scanned Copy of Identification Document",
        ),
    ],
)

consent_section = FormSection(
    title="Consent and Privacy",
    desc=None,
    fields=[
        CheckboxField(
            name="treatmentConsent",
            label="I consent to receive treatment for my health condition.",
        ),
        CheckboxField(
            name="disclosureConsent",
            label="I consent to the use and disclosure of my health information for treatment purposes.",
        ),
        CheckboxField(
            name="privacyConsent",
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
