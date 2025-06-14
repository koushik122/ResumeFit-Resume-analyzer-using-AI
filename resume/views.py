from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DataForm
from .models import Data
import PyPDF2
import resume.nltk_spacy as nltk_spacy
import resume.ai as ai
import markdown


# Create your views here.
def index(request):
    form = None
    if request.method == "POST":
        form = DataForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("result")        
        else:
            messages.error(request, "Please fill out both fields correctly.")
            form = DataForm()
            return render(request, "index.html")

    form = DataForm()
    return render(request, "index.html", {"form": form})


def result(request):

    all_data = Data.objects.latest("id")

    job_description = all_data.job_desc
    print(job_description)

    pdf_path = all_data.resume_file.path

    # Check if the uploaded file is a PDF
    if not pdf_path.lower().endswith(".pdf"):
        messages.error(request, "Only PDF files are supported. Please upload a valid PDF.")
        return redirect("index")

    resume_text = ""
    try:
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                resume_text += page.extract_text()
    except Exception as e:
        messages.error(request, f"Error reading PDF file. Please upload a valid PDF.")
        return redirect("index")
    

    print(resume_text)
    

    def replace_key_of_dict(original_dict):
        updated_dict = {key.replace('-', ' '): value for key, value in original_dict.items()}
        # print(updated_dict)
        return updated_dict
    
    def replace_of_list_item(original_list):
        updated_list = [item.replace('-', ' ') for item in original_list]
        # print(updated_list)
        return updated_list

    
    # spacy and nltk setup

    keywords_resume = nltk_spacy.keyword(resume_text)
    print(f"nltk keyword:  {keywords_resume}")

    # Got a <dict>
    job_desc_tech_unsorted, status_code = ai.job_technical_skill_with_weightage(job_description)
    if not job_desc_tech_unsorted and status_code != 200:
        messages.error(request, "Artificial Intelligence Module is Not Available Right Now. Please Try Again Later.")
        return redirect("index")
    print(job_desc_tech_unsorted)
    print(f"{status_code}\n\n\n\n")
    job_desc_tech_unsorted=replace_key_of_dict(job_desc_tech_unsorted)

    # Got a <dict>
    job_desc_soft_unsorted, status_code = ai.job_soft_skill_with_weightage(job_description)
    if not job_desc_soft_unsorted and status_code != 200:
        messages.error(request, "Artificial Intelligence Module is Not Available Right Now. Please Try Again Later.")
        return redirect("index")
    print(job_desc_soft_unsorted)
    print(f"{status_code}\n\n\n\n")
    job_desc_soft_unsorted=replace_key_of_dict(job_desc_soft_unsorted)

    # Got a <list>
    resume_tech_unsorted, status_code = ai.resume_technical_skill(resume_text)
    if not resume_tech_unsorted and status_code != 200:
        messages.error(request, "Artificial Intelligence Module is Not Available Right Now. Please Try Again Later.")
        return redirect("index")
    print(resume_tech_unsorted)
    print(f"{status_code}\n\n\n\n")
    resume_tech_unsorted=replace_of_list_item(resume_tech_unsorted)

    # Got a <list>
    resume_soft_unsorted, status_code = ai.resume_soft_skill(resume_text)
    if not resume_soft_unsorted and status_code != 200:
        messages.error(request, "Artificial Intelligence Module is Not Available Right Now. Please Try Again Later.")
        return redirect("index")
    print(resume_soft_unsorted)
    print(f"{status_code}\n\n\n\n")
    resume_soft_unsorted=replace_of_list_item(resume_soft_unsorted)


    # Sorting all the keys based on their values
    job_desc_tech = dict(
        sorted(job_desc_tech_unsorted.items(), key=lambda item: item[1], reverse=True)
    )
    job_desc_soft = dict(
        sorted(job_desc_soft_unsorted.items(), key=lambda item: item[1], reverse=True)
    )


    resume_tech = resume_tech_unsorted
    resume_soft = resume_soft_unsorted

    def calculate_scores(job_desc_tech, job_desc_soft, resume_tech, resume_soft):
        # Create lowercase mappings for case-insensitive matching
        job_desc_tech_lower = {
            k.lower(): k for k in job_desc_tech
        }  # Maps lowercase to original key
        job_desc_soft_lower = {k.lower(): k for k in job_desc_soft}

        resume_tech_lower = [skill.lower() for skill in resume_tech]
        resume_soft_lower = [skill.lower() for skill in resume_soft]

        # Matched Technical Skills
        matched_tech = [
            job_desc_tech_lower[skill]
            for skill in resume_tech_lower
            if skill in job_desc_tech_lower
        ]
        unmatched_tech = [
            original
            for lower, original in job_desc_tech_lower.items()
            if lower not in resume_tech_lower
        ]

        # Matched Soft Skills
        matched_soft = [
            job_desc_soft_lower[skill]
            for skill in resume_soft_lower
            if skill in job_desc_soft_lower
        ]
        unmatched_soft = [
            original
            for lower, original in job_desc_soft_lower.items()
            if lower not in resume_soft_lower
        ]

        # Technical Skills Score Calculation
        tech_score = sum(job_desc_tech[skill] for skill in matched_tech)
        max_tech_score = sum(job_desc_tech.values())
        tech_percentage = (
            round((tech_score / max_tech_score) * 100) if max_tech_score > 0 else 0
        )

        # Soft Skills Score Calculation
        soft_score = sum(job_desc_soft[skill] for skill in matched_soft)
        max_soft_score = sum(job_desc_soft.values())
        soft_percentage = (
            round((soft_score / max_soft_score) * 100) if max_soft_score > 0 else 0
        )

        # Total Score Calculation
        total_score = tech_score + soft_score
        max_total_score = max_tech_score + max_soft_score
        total_percentage = (
            round((total_score / max_total_score) * 100) if max_total_score > 0 else 0
        )

        # Combine lists and wrap each word with single quotes
        unmatched_all_skills_string = ",".join(
            f"'{word}'" for word in unmatched_tech + unmatched_soft
        )

        return {
            "tech_score": tech_score,
            "tech_percentage": tech_percentage,
            "matched_tech": matched_tech,
            "unmatched_tech": unmatched_tech,
            "soft_score": soft_score,
            "soft_percentage": soft_percentage,
            "matched_soft": matched_soft,
            "unmatched_soft": unmatched_soft,
            "total_score": total_score,
            "total_percentage": total_percentage,
            "unmatched_all_skills_string": unmatched_all_skills_string,
        }
    
    # Function to format markdown text to HTML
    # This function uses the markdown library to convert raw markdown text to HTML    
    def format_markdown(raw_text):
        html = markdown.markdown(raw_text)
        return html


    result = calculate_scores(job_desc_tech, job_desc_soft, resume_tech, resume_soft)

    text, status_code = ai.suggestion(resume_text, result["unmatched_all_skills_string"])
    print(f"{status_code}\n\n\n\n")
    if not text and  status_code != 200:
        messages.error(request, "Artificial Intelligence Module is Not Available Right Now. Please Try Again Later.")
        return redirect("index")

    cleaned_text = format_markdown(text)


    all_result = {
        "tech_score": result["tech_score"],
        "tech_percentage": result["tech_percentage"],
        "matched_tech": result["matched_tech"],
        "unmatched_tech": result["unmatched_tech"],
        "soft_score": result["soft_score"],
        "soft_percentage": result["soft_percentage"],
        "matched_soft": result["matched_soft"],
        "unmatched_soft": result["unmatched_soft"],
        "total_score": result["total_score"],
        "total_percentage": result["total_percentage"],
        "suggestion": cleaned_text
    }

    return render(request, "result.html", {"all_result": all_result})