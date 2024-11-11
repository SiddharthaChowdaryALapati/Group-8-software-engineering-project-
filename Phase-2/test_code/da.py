import streamlit as st
import pandas as pd
import datetime

# Sample data to simulate the doctors, categories, and bed availability
doctors_data = [
    {"name": "Dr. John Doe", "specialty": "Cardiologist", "availability": ["Monday", "Wednesday", "Friday"]},
    {"name": "Dr. Jane Smith", "specialty": "Dermatologist", "availability": ["Tuesday", "Thursday"]},
    {"name": "Dr. Emily Davis", "specialty": "Pediatrician", "availability": ["Monday", "Thursday"]},
    {"name": "Dr. Mark Lee", "specialty": "Orthopedic", "availability": ["Wednesday", "Friday"]},
]

beds_data = {
    "ICU": 2,
    "General": 5,
    "Private": 3
}

appointments = []

# Convert sample data to DataFrame
doctors_df = pd.DataFrame(doctors_data)

# Streamlit UI
def main():
    st.title("Hospital Appointment and Bed Availability System")

    # Section for scheduling an appointment
    st.header("Schedule a Doctor's Appointment")
    patient_name = st.text_input("Enter Patient Name")
    patient_age = st.number_input("Enter Patient Age", min_value=0)
    patient_contact = st.text_input("Enter Patient Contact Number")
    specialty = st.selectbox("Select Specialty", doctors_df["specialty"].unique())
    available_doctors = doctors_df[doctors_df["specialty"] == specialty]
    doctor = st.selectbox("Select Doctor", available_doctors["name"])
    appointment_date = st.date_input("Select Appointment Date", min_value=datetime.date.today())
    appointment_time = st.time_input("Select Appointment Time")
    appointment_day = appointment_date.strftime("%A")

    # Check doctor's availability
    selected_doctor = available_doctors[available_doctors["name"] == doctor].iloc[0]
    if appointment_day in selected_doctor["availability"]:
        if st.button("Schedule Appointment"):
            appointment = {
                "patient_name": patient_name,
                "patient_age": patient_age,
                "patient_contact": patient_contact,
                "doctor": doctor,
                "specialty": specialty,
                "date": appointment_date,
                "time": appointment_time
            }
            appointments.append(appointment)
            st.success(f"Appointment scheduled with {doctor} ({specialty}) on {appointment_date} at {appointment_time}.")
    else:
        st.error(f"{doctor} is not available on {appointment_day}. Please select a different date.")

    # Display scheduled appointments
    st.header("Scheduled Appointments")
    if len(appointments) > 0:
        appointments_df = pd.DataFrame(appointments)
        st.table(appointments_df)
    else:
        st.info("No appointments scheduled.")

    # Section for checking bed availability
    st.header("Check Bed Availability")
    bed_category = st.selectbox("Select Bed Category", list(beds_data.keys()), key="bed_category")
    if st.button("Check Bed Availability"):
        available_beds = beds_data[bed_category]
        if available_beds > 0:
            st.success(f"{available_beds} {bed_category} bed(s) available.")
        else:
            st.error(f"No {bed_category} beds available.")

    # Section for bed booking
    st.header("Book a Bed")
    patient_name_bed = st.text_input("Enter Patient Name for Bed Booking", key="bed_booking")
    bed_category_booking = st.selectbox("Select Bed Category for Booking", list(beds_data.keys()), key="bed_booking_category")
    if st.button("Book Bed"):
        if beds_data[bed_category_booking] > 0:
            beds_data[bed_category_booking] -= 1
            st.success(f"Bed booked successfully for {patient_name_bed} in {bed_category_booking} category.")
        else:
            st.error(f"No {bed_category_booking} beds available for booking.")

if __name__ == "__main__":
    main()
