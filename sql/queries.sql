-- View all records from the hospital patients table
select * from hospital_patients;

-- Which departments generated the highest revenue and treated the most patients?
select department,count(patientid) as total_patients,sum(billamount) as total_revenue
from hospital_patients
group by department
order by total_revenue;

-- How many patients were diagnosed with each condition and what was their average length of stay?
select diagnosis,count(patientid) as total_patients,avg(lengthofstay) as los
from hospital_patients
group by diagnosis;

-- How many admissions and how much revenue were generated each month?
select admissionmonth,count(patientid) as total_admissions,round(sum(billamount),0) as total_revenue
from hospital_patients
group by admissionmonth
order by total_admissions;

-- Who are the top 10 patients with the highest hospital bills?
select patientid,patientname,department,diagnosis,billamount as bill
from hospital_patients
order by bill desc
limit 10;

-- Which insurance types contribute the most patients and revenue?
select insurancetype,count(patientid) as total_patients,sum(billamount) as revenue
from hospital_patients
group by insurancetype
order by revenue desc;

-- What is the patient distribution and revenue contribution by gender?
select gender,count(patientid) as total_patients,sum(billamount) as revenue
from hospital_patients
group by gender
order by total_patients desc;

-- How many patients were admitted under each admission type and what is the average bill amount?
select admissiontype,count(patientid) as total_patients,round(avg(billamount),0) as revenue
from hospital_patients
group by admissiontype
order by total_patients desc;

-- What is the distribution of patients by discharge status?
select dischargestatus,count(patientid) as total_patients
from hospital_patients
group by dischargestatus
order by total_patients desc;

-- Which doctors handled the highest number of patients in each department?
select doctorname,department,count(patientid) as total_patients
from hospital_patients
group by doctorname,department
order by total_patients desc;

-- What is the total billed amount and patient count by payment status?
select paymentstatus,count(patientid) as total_patients,
round(sum(billamount),0) as total_amount_billed
from hospital_patients
group by paymentstatus
order by total_amount_billed desc;

-- Which diagnosis and department combinations have the highest average treatment cost?
select diagnosis,department,
count(patientid) as total_patients,
round(avg(billamount),0) as avg_bill,
round(max(billamount),0) as highest_bill,
round(min(billamount),0) as lowest_bill
from hospital_patients
group by diagnosis,department
order by avg_bill desc
limit 5;

-- Do more patient admissions occur on weekdays or weekends?
select
   case
      when EXTRACT(DOW from admissiondate::DATE) in (0,6) then 'weekend'
      else 'weekday'
   end as day_of_the_week,
   count(patientid) as total_admissions
from hospital_patients
group by day_of_the_week
order by total_admissions desc;

-- What is the readmission count and readmission rate for each department?
select department,
   count(patientid) as total_patients,
   sum(
      case
         when readmissionwithin30days = 'Yes' then 1
         else 0
      end) as readmitted_count,
   sum(
      case
         when readmissionwithin30days = 'Yes' then 1
         else 0
      end) * 100 / count(patientid) as readmission_rate
from hospital_patients
group by department;

-- How are patients and revenue distributed across different age groups?
select
   case
      when age between 0 and 17 then 'child'
      when age between 18 and 35 then 'Teen'
      when age between 35 and 70 then 'senior'
      else '71 and above elderly'
   end as age_group,
   count(patientid) as total_patients,
   sum(billamount) as total_revenue
from hospital_patients
group by age_group
order by total_revenue desc;

-- What are the patient count, total revenue, and average bill per patient for each department?
select
    department,
    count(patientid) as total_patients,
    round(sum(billamount),0) as total_revenue,
    round(avg(billamount),0) as avg_bill_per_patient
from hospital_patients
group by department
order by total_revenue desc;

-- Create a department performance dashboard showing patients, revenue, LOS, readmissions, and recovery metrics
select
    department,
    count(patientid) as total_patients,
    round(sum(billamount),0) as total_revenue,
    round(avg(billamount),0) as avg_bill,
    round(avg(lengthofstay),1) as avg_los_days,
    sum(
        case
            when readmissionwithin30days = 'Yes' then 1
            else 0
        end) as total_readmissions,
    round(
        sum(
            case
                when readmissionwithin30days = 'Yes' then 1
                else 0
            end
        ) * 100.0 / count(patientid),1
    ) as readmission_rate_pct,
    sum(
        case
            when dischargestatus = 'Recovered' then 1
            else 0
        end
    ) as recovered_patients
from hospital_patients
group by department
order by total_revenue desc;
