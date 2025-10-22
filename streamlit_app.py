import streamlit as st
import pandas as pd
import uuid
import math
import plotly.express as px  

# --- Page configuration ---
st.set_page_config(
    page_title="ROI and Cost Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"  # Keep sidebar open
)

# --- Define pages and hierarchy ---
PAGE_GROUPS = {
    "Instructions": [],
    "Inputs": {
        "Personnel Costs": [],
        "Infrastructure Costs": [],
        "ROI Parameters": [],
        "Project Activities": ["Business as Usual", "Proposed Tool"],
    },
    "Outputs": {
        "Project-Stage Efficiency Gains": [],
        "Personnel Efficiency Gains": [],
        "ROI": []
    }
}

# Flatten pages for sequential navigation
PAGES = [
    "Instructions",
    "Personnel Costs",
    "Infrastructure Costs",
    "ROI Parameters",
    "Business as Usual",
    "Proposed Tool",
    "Project-Stage Efficiency Gains",
    "Personnel Efficiency Gains",
    "ROI"
]

# --- Initialize session state ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Instructions"

# --- Sidebar Navigation ---
st.sidebar.title("Navigation")

if st.sidebar.button("Instructions", use_container_width=True):
    st.session_state.current_page = "Instructions"

st.sidebar.markdown("### 🧩 Inputs")
for page_name, subpages in PAGE_GROUPS["Inputs"].items():
    # Only Project Activities has subpages
    if page_name == "Project Activities":
        st.sidebar.markdown(f"**{page_name}**")  # Label, not clickable
        for sub in subpages:
            if st.sidebar.button(f" {sub}", use_container_width=True):
                st.session_state.current_page = sub
    else:
        if st.sidebar.button(f"{page_name}", use_container_width=True):
            st.session_state.current_page = page_name

st.sidebar.markdown("### 📊 Outputs")
for page_name, subpages in PAGE_GROUPS["Outputs"].items():
    if st.sidebar.button(f"{page_name}", use_container_width=True):
        st.session_state.current_page = page_name

# --- Helper functions ---
def go_next():
    idx = PAGES.index(st.session_state.current_page)
    if idx < len(PAGES) - 1:
        st.session_state.current_page = PAGES[idx + 1]

def go_back():
    idx = PAGES.index(st.session_state.current_page)
    if idx > 0:
        st.session_state.current_page = PAGES[idx - 1]

def go_first():
    st.session_state.current_page = PAGES[0]

# --- CSS for fixed nav buttons ---
st.markdown("""
<style>
.nav-buttons {
    position: fixed;
    bottom: 20px;
    left: 0;
    right: 0;
    background-color: rgba(255, 255, 255, 0.9);
    padding: 10px 20px;
    border-top: 1px solid #ddd;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 9999;
}
</style>
""", unsafe_allow_html=True)

# --- Initialize session state for storing activity data ---
if "project_steps" not in st.session_state:
    st.session_state.project_steps = {
        "BAU": {},
        "Proposed Tool": {}
    }

# --- Example personnel list (from Personnel Salaries) ---
if "personnel_rows" not in st.session_state:
    st.session_state.personnel_rows = [
        {"Role": "Engineer"},
        {"Role": "Researcher"},
        {"Role": "Project Manager"}
    ]

personnel_roles = [p["Role"] for p in st.session_state.personnel_rows]

# --- Project stages ---
project_stages = [
    "Data Agreements and Research Approvals",
    "Data Collection & Access or Transfer",
    "Study Design & Infrastructure Setup",
    "Study Implementation and Monitoring",
    "Data Modeling & Analysis",
    "Reporting"
]

# --- Helper function to render activity sections ---
def render_activity_section(section_name):
    # List to collect all preview data
    all_preview_data = []

    for stage in project_stages:
        with st.expander(stage, expanded=False):
            # Initialize storage with prefilled steps if empty
            if stage not in st.session_state.project_steps[section_name]:
                st.session_state.project_steps[section_name][stage] = []

                # Stage-specific prefilled steps
                if stage == 'Data Agreements and Research Approvals':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                        "id": str(uuid.uuid4()),
                        "Step": "Drafting agreements, review, executing DSAs and DUAs",
                        "Notes": "",
                        "Duration": 0.0,
                        "Roles": {r: 0.0 for r in personnel_roles}},
                                                {
                            "id": str(uuid.uuid4()),
                            "Step": "Researchers to complete IRB requirements",
                            "Notes": "",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        },
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Consenting Participants",
                            "Notes": "e.g. Obtaining consent from users / students using the curriculum platform through ToS, pop-up or checkbox, or another form of notification",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                        ]
                elif stage == 'Data Collection & Access or Transfer':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Data Collection, Documentation, Anonymization (i.e. Data setup)",
                            "Notes": "e.g. Collecting individual observations. Data querying and extraction: querying, verification, troubleshooting. Data anonymization, establishing protocol, implementation, review. Data documentation: data dictionary, access instructions. Final review",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        },
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Secure data access / transfer to researchers",
                            "Notes": "e.g. District may share data through file storage solution (e.g. CSVs on Microsoft SharePoint). Setup requires account setup, transferring data, configuring permissions. Education platform shares data via access to certain tables or views on their database. Setup may require VPN setup for an external user, configure persmissions, test & verify. Researcher: may need to install certain software and configure their system to securely access the data shared.",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                elif stage == 'Study Design & Infrastructure Setup':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Data Prep and Exploration",
                            "Notes": "e.g. "
                            "Researcher may review, clean, merge and validate datasets. District/Platform may answer data questions and fix issues as needed."
                            " Researcher will also compile analyses to understand data distributions, run power calculations, determine randomization strategy, etc. to guide study design.",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        },
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Data preparation to implement the study",
                            "Notes": "e.g. if it is an A/B testing study, you may need to develop the content or implement feature changes to the educational platform which may include: create / update / review content, create variants (for A/B testing), update database / UI changes",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        },
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Setting up the infrastructure to execute or run the experiment",
                            "Notes": "e.g. if it is an A/B testing study, and you are setting up A/B testing operations for the first time, you may need to: setup the database, setup the data pipeline to ingest, process, and analyze data, build a dashboard to report analytics or metrics, integrate the data or study content into the platform, test or validate the platform (QA checks), prepare documentation or training sessions",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                elif stage == 'Study Implementation and Monitoring':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Run the study",
                            "Notes": "e.g. Run a pilot study (i.e. testing that the A/B testing works as expected) before scaling to entire data sample. Running the actual study. Periodic data sharing and monitoring over the study implementation period.",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                elif stage == 'Data Modeling & Analysis':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Analysis & QA",
                            "Notes": "e.g. verify that the experiment was conducted correctly, statistcal analyses or models (e.g. using Machine Learning) to analyze data, interpret findings, produce descriptives or graphs",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                elif stage == 'Reporting':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Report writing & communications",
                            "Notes": "e.g. setup a dashboard communicate results, publish research paper / whitepaper, blog post, disseminate findings to broader community, proposal for next steps",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                else:
                    st.session_state.project_steps[section_name][stage] = [{
                        "id": str(uuid.uuid4()),
                        "Step": "",
                        "Notes": "",
                        "Duration": 0.0,
                        "Roles": {r: 0.0 for r in personnel_roles}
                    }]

            rows = st.session_state.project_steps[section_name][stage]

            for idx, row in enumerate(rows.copy()):
                st.markdown(f"<span style='color:#DF7861; font-weight:bold;'>**Step {idx+1}**</span>", unsafe_allow_html=True)

                # Step Description + Notes
                cols1 = st.columns([4, 4])
                step_desc = cols1[0].text_area(
                    "Step Description",
                    value=row.get("Step", ""),
                    key=f"{section_name}_{stage}_step_{row['id']}",
                    height=80
                )
                notes = cols1[1].text_area(
                    "Notes",
                    value=row.get("Notes", ""),
                    key=f"{section_name}_{stage}_notes_{row['id']}",
                    height=80
                )
                row.update({"Step": step_desc, "Notes": notes})

                # Duration
                cols2 = st.columns([2])
                duration = cols2[0].number_input(
                    "Total Duration (weeks)",
                    min_value=0.0,
                    step=1.0,
                    format="%.2f",
                    value=row.get("Duration", 0.0),
                    key=f"{section_name}_{stage}_dur_{row['id']}"
                )
                
                row["Duration"] = duration

                # Active time % per role
                st.markdown(f"<span style='color:#ECB390;'>*% Active Time Spent per Role*</span>", unsafe_allow_html=True)
                time_data = {}
                roles_per_row = 5
                for i in range(0, len(personnel_roles), roles_per_row):
                    role_subset = personnel_roles[i:i + roles_per_row]
                    
                    # Create 5 equal-width columns no matter how many roles are in this subset
                    cols = st.columns(roles_per_row)

                    for j, role in enumerate(role_subset):
                        with cols[j]:
                            val = st.number_input(
                                f"{role}",
                                min_value=0.0,
                                step=1.0,
                                value=row.get("Roles", {}).get(role, 0.0),
                                format="%.2f",
                                key=f"{section_name}_{stage}_{role}_{row['id']}"
                            )
                            time_data[role] = val

                    # Fill remaining columns with empty space if fewer than 5 roles
                    for j in range(len(role_subset), roles_per_row):
                        with cols[j]:
                            st.markdown("")  # keeps layout aligned
                row["Roles"] = time_data

                # Delete Step
                if st.button("❌ Delete", key=f"del_{section_name}_{stage}_{row['id']}"):
                    st.session_state.project_steps[section_name][stage] = [
                        r for r in rows if r["id"] != row["id"]
                    ]
                    st.rerun()
                    
                st.markdown("---")

            # Add new step
            if st.button(f"➕ Add Step to {stage}", key=f"add_{section_name}_{stage}"):
                new_row = {
                    "id": str(uuid.uuid4()),
                    "Step": "",
                    "Notes": "",
                    "Duration": 0.0,
                    "Roles": {r: 0.0 for r in personnel_roles}
                }
                st.session_state.project_steps[section_name][stage].append(new_row)
                st.rerun()

            # Collect stage data for final preview
            for r in st.session_state.project_steps[section_name][stage]:
                for role, active_time in r["Roles"].items():
                    all_preview_data.append({
                        "Stage": stage,
                        "Step": r["Step"],
                        "Notes": r["Notes"],
                        "Total Duration (weeks)": r["Duration"],
                        "Role": role,
                        "Active Time Spent (%)": active_time
                    })

    # --- Final consolidated preview table ---
    if all_preview_data:
        st.markdown(f"### {section_name} Activities")
        df = pd.DataFrame(all_preview_data)
        st.dataframe(df, use_container_width=True)
        # --- Save the final table in session state for computations ---
        st.session_state[f"df_{section_name.replace(' ', '_')}"] = df

def copy_from_section(source_section, target_section):
    """Copy all steps from a source section to the target section."""
    if source_section in st.session_state.project_steps:
        st.session_state.project_steps[target_section] = {}
        for stage, steps in st.session_state.project_steps[source_section].items():
            copied_steps = []
            for step in steps:
                copied_steps.append({
                    "id": str(uuid.uuid4()),  # new UUID for the copied step
                    "Step": step["Step"],
                    "Notes": step["Notes"],
                    "Duration": step["Duration"],
                    "Roles": step["Roles"].copy()
                })
            st.session_state.project_steps[target_section][stage] = copied_steps
        st.success(f"✅ All values copied from {source_section} to {target_section}!")
    else:
        st.warning(f"⚠️ No data found in {source_section} to copy.")

def compute_projection(
    scenario_name, 
    time_months, 
    cost_per_study, 
    impact_per_study, 
    fixed_cost, 
    num_orgs, 
    num_concurrent_projects=1
):
    """
    Computes a 50-year projection of costs, impact, and ROI for a research scenario.

    Parameters:
    - scenario_name (str): Name of the scenario (e.g., "Business as Usual", "Proposed Tool").
    - time_months (float): Duration of a single study in months.
    - cost_per_study (float): Variable cost per study.
    - impact_per_study (float): Impact (in $) per study.
    - fixed_cost (float): Fixed 1-time setup cost for the scenario.
    - num_orgs (int): Number of organizations conducting studies.
    - num_concurrent_projects (int, default=1): Number of studies each org runs concurrently.

    Returns:
    - projection_data (list of dict): List containing annual projections of costs, impact, and ROI.
    """

    projection_data = []
    for year in range(1, 51):  # 50-year projection
        total_months = year * 12

        # Compute number of studies each organization can conduct in this year
        if time_months > 0:
            studies_each_org = math.floor(total_months * num_concurrent_projects / time_months)
        else:
            studies_each_org = 0  # Avoid division by zero

        # Compute costs
        variable_cost = cost_per_study * studies_each_org * num_orgs
        total_cost = variable_cost + fixed_cost

        # Compute total impact
        impact = impact_per_study * studies_each_org * num_orgs

        # Compute ROI
        roi_excl_fc = impact / variable_cost if variable_cost > 0 else 0
        roi_incl_fc = impact / total_cost if total_cost > 0 else 0

        # Append data for this year
        projection_data.append({
            "Scenario": scenario_name,
            "Year": year,
            "# of studies per org": studies_each_org,
            "Fixed Cost ($)": fixed_cost,
            "Variable Cost ($)": variable_cost,
            "Total Cost ($)": total_cost,
            "Impact ($)": impact,
            "Impact per $ (Variable only)": roi_excl_fc,
            "Impact per $ (Total cost)": roi_incl_fc
        })

    return projection_data

# Extract scenario values from ROI summary
def get_scenario_value(scenario, col):
    try:
        return roi_df.loc[roi_df["Scenario"] == scenario, col].values[0]
    except:
        return 0


# --- Main Page ---
st.title("ROI and Cost Analysis Dashboard")
page = st.session_state.current_page


# =========================================================
# =========================================================
#  PAGE CONTENTS
# =========================================================
# =========================================================

# =========================================================
#  INSTRUCTIONS PAGE
# =========================================================
if page == "Instructions":
    st.info(""" 
            ### What is the purpose of this tool? ###
            This tool was designed to help ed-tech non-profits and grantee organizations measure the value and impact of investing in building tools to support research on their platforms. It estimates potential efficiency gains, cost savings, and return on investment (ROI) from developing tools such as integrated data systems, scalable experimentation environments, and automated analysis solutions.
            
            **Goals**
            - Establish a standardized framework for calculating efficiency gains across organizations.
            - Offer data-driven comparisons between current research processes and those improved by the proposed tool.
            - Provide clear, evidence-based insights to help both funders and non-profits understand the ROI and long-term impact of their investments.
            """)
    

    st.markdown("---")
    st.markdown("## ⚙️ Instructions")
    st.markdown("---")

    st.subheader("Before you begin")
    st.markdown("""
    - Before getting started, make sure you have a clear understanding of the types of research projects your proposed tool supports.
        - For example, if you're developing an A/B testing platform to evaluate ed-tech interventions, a relevant research project might involve testing student performance on math questions with and without AI-generated hints.
    - Consider all the key roles involved in implementing such a study, such as data engineers, data scientists, project managers, and research leads.
    - Also consider the key steps in conducting the research, including tasks like establishing data-sharing agreements, obtaining student consent, managing data storage and security, random sampling, conducting analysis, and writing and disseminating the final report.
    - Finally, think about which steps in the research process - and which roles involved - your proposed tool helps make more efficient, and how it does so. Consider the specific challenges your tool aims to solve, such as reducing manual effort, improving data accessibility, streamlining collaboration, or accelerating analysis and reporting.
    - This tool guides you through the process by comparing how a research project operates today (**Business as Usual** Scenario) versus how it would function with the tool in place (**Proposed Tool** Scenario).""")

    # st.subheader("▶️ Tutorial Video")
    # st.video("https://www.youtube.com/watch?v=_4kHxtiuML0")  # replace with your link

    st.subheader("Steps")
    st.markdown("""
    1. **Use the Sidebar** to navigate between pages.  
    2. **Enter the Input Data**
        - **Personnel Costs**: Specify the roles/personnel and salaries involved in conducting the research project
        - **Infrastructure Costs**: Specify the non-personnel cost (e.g. hardware, software, storage, API usage) required to conduct the research project in both **Business as Usual** and **Proposed Tool** scenarios.
        - **ROI Parameters**: Fill in the relevant metrics to conduct an ROI analysis for both scenarios (e.g. Number of research organizations supported concurrently, Total investment by grantees, Estimated impact of a single research project)
    3. **Project Activities**
        - **Business as Usual**: Consider how the research project would run **without** the proposed tool. For each stage of the project, describe the steps involved and estimate the total time and personnel effort required. If a stage doesn't apply, you can leave it blank.
        - **Proposed Tool**: Consider how the research project would run **with** the proposed tool. For each stage of the project, describe the steps involved and estimate the total time and personnel effort required. If a stage doesn't apply, you can leave it blank. To simplify, you can **copy estimates from the Business as Usual scenario** and make edits only for the stages where the proposed tool is expected to change time or personnel effort.
    4. **View Outputs**
        - **Project-Stage Efficiency Gains**: Time and cost savings for a single research project using the proposed tool, broken down by research project stage. These values are automatically calculated based on input data.
        - **Personnel Efficiency Gains**:  Time and cost savings for a single research project using the proposed tool, broken down by personnel/roles involved. These values are automatically calculated based on input data.
        - **ROI**: Return on investment for grantee organizations, scaled by the estimated number of organizations supported in the Business as Usual vs. Proposed Tool scenarios.
    5. Use **Next** and **Back** buttons for step-wise navigation.
    """)

# =========================================================
#  PERSONNEL SALARIES PAGE
# =========================================================
elif page == "Personnel Costs":
    st.markdown("---")
    st.header("💼 Personnel Costs")
    st.markdown("---")

    # Ensure session state exists and all rows have required keys
    if "personnel_rows" not in st.session_state:
        st.session_state.personnel_rows = []

    # Fill default rows if empty
    if len(st.session_state.personnel_rows) == 0:
        st.session_state.personnel_rows = [
            {"id": str(uuid.uuid4()), "Role": "Engineer", "Average Hourly Rate": 65.0, "Notes": "e.g. Software or Data Engineer"},
            {"id": str(uuid.uuid4()), "Role": "Researcher", "Average Hourly Rate": 25.0, "Notes": "e.g. PhD student"},
            {"id": str(uuid.uuid4()), "Role": "Project Manager", "Average Hourly Rate": 48.0, "Notes": "e.g. Partnerships or research manager"},
        ]

    rows = st.session_state.personnel_rows

    for idx, row in enumerate(rows):
        # Ensure all keys exist in case of malformed rows
        row.setdefault("id", str(uuid.uuid4()))
        row.setdefault("Role", "")
        row.setdefault("Average Hourly Rate", 0.0)
        row.setdefault("Notes", "")

        st.markdown(f"<span style='color:#DF7861'>***Personnel {idx+1}***</span>", unsafe_allow_html=True)

        cols = st.columns([4, 3, 7, 1])  # Narrow column for trash icon

        # Editable inputs
        role = cols[0].text_input("Role", row["Role"], key=f"role_{row['id']}")
        rate = cols[1].number_input("Hourly Rate ($)", min_value=0.0,
                                    value=row["Average Hourly Rate"],
                                    step=1.0,
                                    key=f"rate_{row['id']}")
        notes = cols[2].text_input("Notes", row["Notes"], key=f"notes_{row['id']}")

        # Delete button
        if cols[3].button("❌", key=f"del_{row['id']}"):
            st.session_state.personnel_rows = [r for r in rows if r["id"] != row["id"]]
            st.rerun()

        # Update row in session state
        row.update({"Role": role, "Average Hourly Rate": rate, "Notes": notes})

    # Add new row
    if st.button("➕ Add Row"):
        st.session_state.personnel_rows.append({
            "id": str(uuid.uuid4()), "Role": "", "Average Hourly Rate": 0.0, "Notes": ""
        })
        st.rerun()

    # Display summary
    st.write("### Personnel Costs Table")
    personnel_salaries_df = pd.DataFrame(st.session_state.personnel_rows).drop(columns="id")
    st.dataframe(personnel_salaries_df, use_container_width=True)
    st.session_state[f"df_personnel_salaries"] = personnel_salaries_df

# =========================================================
#  PROJECT ACTIVITIES PAGE
# =========================================================
elif page == "Business as Usual":
    st.markdown("---")
    st.header("📊 Project Activities: *Business as Usual Scenario*")
    st.markdown("---")
    st.caption(
        "Overall project stage titles remain unchanged to serve as consistent framework across projects." \
        " The steps listed under each project stage are intended as a guiding framework to help you complete this section. You may edit, add, or delete the steps under each project stage so that they align with the types of projects your tool supports. "
        " " \
        "Please note: deleting a step means it is not required to complete the research project. Even if your proposed tool does not target a particular step, the step must be included if it is relevant to conducting the research project."
        " You may also include any additional notes related to the execution of each project step. This is particularly useful in the ***Proposed Tool*** scenario to explain why a step shows a significant difference in total time or personnel effort compared to ***Business as Usual***."
    )
    render_activity_section("BAU")

elif page == "Proposed Tool":
    st.markdown("---")
    st.header("📊 Project Activities: *Proposed Tool*")
    st.markdown("---")
    st.caption(
        "Overall project stage titles remain unchanged to serve as consistent framework across projects." \
        " The steps listed under each project stage are intended as a guiding framework to help you complete this section. You may edit, add, or delete the steps under each project stage so that they align with the types of projects your tool supports. "
        " Please note: deleting a step means it is not required to complete the research project. Even if your proposed tool does not target a particular step, the step must be included if it is relevant to conducting the research project."
        " You may include any additional notes related to the execution of each project step. This is particularly useful in the ***Proposed Tool*** scenario to explain why a step shows a significant difference in total time or personnel effort compared to ***Business as Usual***."
    )

    if st.button(
        "📋 Pre-Fill estimates from Business as Usual",
        help="Copy all estimates from the Business as Usual scenario to save time. You can then adjust only where the proposed tool changes things.",
        key="pre_fill_button"
    ):
        copy_from_section("Business as Usual", "Proposed Tool")

    render_activity_section("Proposed Tool")

# =========================================================
#  ROI PARAMETERS PAGE
# =========================================================
elif page == "ROI Parameters":
    st.markdown("---")
    st.header("📈 ROI Parameters")
    st.markdown("---")

    # --- Median Impact on Learning Outcomes ---
    st.markdown("<h3 style='color:#ECB390;'>Estimated Impact of Research Project</h3>", unsafe_allow_html=True)


    # --- Primary Outcome ---
    col1, col2 = st.columns([3, 2])
    with col1:
        learning_definition = st.text_input(
            "Primary outcome used to evaluate research project impact",
            value="Standardized math scores in middle school",
            help="Specify the outcome that a research project supported by the proposed tool is evaluated on to measure effectiveness or success."
        )
    with col2:
        learning_sd = st.number_input(
            "Median impact (SD)",
            min_value=0.0,
            value=0.12,
            step=0.01,
            format="%.2f",
            key="roi_learning_sd",
            help='Specify estimated median impact in standard deviations. Cross-reference relevant literature.'
        )

    # Add spacing
    st.write("")

    # --- Economic Opportunity Coefficient ---
    col1, col2 = st.columns([3, 2])
    with col1:
        econ_definition = st.text_input(
            "Long-term economic opportunity outcome",
            help="Specify the long-term economic outcome that the primary outcome influences",
            value="Income at age 30"
        )
    with col2:
        econ_per_sd = st.number_input(
            "Average increase per 1 SD improvement ($)",
            min_value=0.0,
            value=2400.0,
            step=0.1,
            format="%.2f",
            help="Enter the expected average increase in the long-term economic opportunity outcome for a 1 standard deviation improvement in the primary outcome",
            key="roi_econ_per_sd"
        )

    # Add spacing after
    st.write("")


    # --- Per-Student Outcome Improvement (Computed) ---
    computed_improvement = learning_sd * econ_per_sd
    st.number_input("Per-student improvement in long-term economic opportunity (in $)", value=computed_improvement,
                    disabled=True)

    # --- Evidence Generation ---
    st.markdown("<h3 style='color:#ECB390;'>Discovery Rate</h3>", unsafe_allow_html=True)
    evidence_rate = st.number_input(
        "Rate of discovery of impact (%)",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=1.0,
        format="%.2f",
        key="roi_evidence_rate",
        help="The estimated probability that a research project will detect measurable impact in the primary outcome"
    )

    # --- Research Study Reach & Investment ---
    st.markdown("<h3 style='color:#ECB390;'>Reach and Impact</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        total_students = st.number_input(
            "Total reach of the research study (number of individuals impacted).",
            min_value=1,
            step=1,
            key="roi_total_students",
            help="Enter the total number of individuals affected by the research project. E.g., the number of students on the ed-tech platform that implements a research intervention."
        )

    with col2:
        total_investment = st.number_input(
            "Total investment by grant organization in the tool (in $)",
            min_value=0,
            step=1000,
            format="%d",
            key="roi_total_investment_k"
        )

    # --- Organizations Served (side by side) ---
    col1, col2, col3 = st.columns(3)

    with col1:
        orgs_bau1 = st.number_input(
            "Orgs supported (Business as Usual)",
            min_value=1,
            step=1,
            value=1,
            key="roi_orgs_bau1",
            help=(
                "Specify the number of organizations that can use the solution in the Business as Usual scenario. "
                "The total number of concurrent projects depends on:\n"
                "- The number of organizations using the solution (BAU or proposed tool).\n"
                "- The number of projects each organization can run concurrently."
            )
        )

    with col2:
        orgs_proposed = st.number_input(
            "Orgs supported (Proposed Tool)",
            min_value=1,
            step=1,
            value=1,
            key="roi_orgs_proposed",
            help=(
                "Specify the number of organizations that can use the solution in the Proposed Tool scenario. "
                "The total number of concurrent projects depends on:\n"
                "- The number of organizations using the solution (BAU or proposed tool).\n"
                "- The number of projects each organization can run concurrently."
            )
        )

    with col3:
        studies_proposed = st.number_input(
            "Concurrent research projects per org",
            min_value=1,
            value=1,
            step=1,
            key="roi_studies_proposed",
            help=(
                "Specify how many research studies each organization can run at the same time using the solution. "
                "The total number of concurrent studies depends on:\n"
                "- The number of organizations using the solution (BAU or proposed tool).\n"
                "- The number of studies each organization can run concurrently."
            )
        )

    # --- Save all ROI parameters in session_state for later use ---
    st.session_state.roi_parameters = {
        "learning_definition": learning_definition,
        "learning_sd": learning_sd,
        "econ_definition": econ_definition,
        "econ_per_sd": econ_per_sd,
        "computed_improvement": computed_improvement,
        "evidence_rate": evidence_rate,
        "total_students": total_students,
        "total_investment": total_investment,
        "orgs_proposed": orgs_proposed,
        "orgs_bau1": orgs_bau1,
        "studies_proposed": studies_proposed
    }

# =========================================================
#  ASSUMPTIONS PAGES
# =========================================================
elif page == "Assumptions":
    st.markdown("---")
    st.header("🧩 Assumptions")
    st.markdown("---")

    st.caption("List any assumptions made during your analysis below. "
               "You can add multiple entries, edit or delete them, and download the full list as a CSV file. This list is for your reference only, it is not used in any calculations.")

    # Initialize session state
    if "assumptions" not in st.session_state:
        st.session_state.assumptions = [
            {"id": str(uuid.uuid4()), "Assumption": "e.g., A/B testing on the platform runs for 4 weeks."}
        ]

    # Display and edit assumptions
    rows = st.session_state.assumptions
    for idx, row in enumerate(rows):
        cols = st.columns([8, 1])
        assumption_text = cols[0].text_input(
            f"Assumption #{idx + 1}",
            value=row["Assumption"],
            key=f"assumption_{row['id']}"
        )
        row["Assumption"] = assumption_text

        # Delete button
        if cols[1].button("❌", key=f"del_assumption_{row['id']}"):
            st.session_state.assumptions = [r for r in rows if r["id"] != row["id"]]
            st.rerun()

    # Add new assumption
    if st.button("➕ Add New Assumption"):
        st.session_state.assumptions.append({
            "id": str(uuid.uuid4()),
            "Assumption": ""
        })
        st.rerun()

    # Display table
    st.markdown("### Current List of Assumptions")
    df_assumptions = pd.DataFrame(st.session_state.assumptions).drop(columns="id")
    st.dataframe(df_assumptions, use_container_width=True)

    # CSV download
    # csv = df_assumptions.to_csv(index=False).encode("utf-8")
    # st.download_button(
    #     label="📥 Download Assumptions as CSV",
    #     data=csv,
    #     file_name="assumptions.csv",
    #     mime="text/csv"
    # )

# =========================================================
#  INFRASTRUCTURE PAGE
# =========================================================
elif page == "Infrastructure Costs":
    st.markdown("---")
    st.header("💻 Infrastructure Costs")
    st.markdown("---")

    st.caption(
        "Enter the per-study **infrastructure costs** (e.g., hardware, software, storage, API usage) for both the Business as Usual and Proposed Tool scenarios. "
        "These are non-personnel operational costs. While research organizations typically pay for subscriptions or services shared across multiple research projects, please provide your best estimate for **per-study costs**. "
        "The cost categories listed below serve as a guiding framework. You may edit, add, or delete categories, adjust amounts, and add notes as needed. "
        "The estimates represent the **total infrastructure cost** from the perspective of a single end user — i.e., a research organization supported by the proposed tool."
    )

    # --- Initialize with prefilled categories but no costs ---
    if "infrastructure_costs" not in st.session_state:
        st.session_state.infrastructure_costs = [
            {
                "id": str(uuid.uuid4()),
                "Cost Category": "Integration Costs",
                "Business as Usual ($)": 0.0,
                "Proposed Tool ($)": 0.0,
                "Notes": "e.g. Proposed tool requires API integration with the organization's codebase."
            },
            {
                "id": str(uuid.uuid4()),
                "Cost Category": "Software Licenses",
                "Business as Usual ($)": 0.0,
                "Proposed Tool ($)": 0.0,
                "Notes": "e.g. Researchers require Stata for analysis."
            },
            {
                "id": str(uuid.uuid4()),
                "Cost Category": "Compute Resources",
                "Business as Usual ($)": 0.0,
                "Proposed Tool ($)": 0.0,
                "Notes": "e.g. Researchers require GPUs for big data analysis."
            },
            {
                "id": str(uuid.uuid4()),
                "Cost Category": "Storage",
                "Business as Usual ($)": 0.0,
                "Proposed Tool ($)": 0.0,
                "Notes": "e.g. Researchers require cloud storage for data access."
            }
        ]

    # --- Editable Cost Inputs ---
    rows = st.session_state.infrastructure_costs
    for idx, row in enumerate(rows):
        st.markdown(f"<span style='color:#DF7861'>***Cost Item {idx + 1}***</span>", unsafe_allow_html=True)

        cols = st.columns([3, 2, 2, 3, 1])
        category = cols[0].text_input(
            "Cost Category",
            value=row["Cost Category"],
            key=f"cat_{row['id']}"
        )
        BAU = cols[1].number_input(
            "Business as Usual ($)",
            min_value=0.0,
            step=10.0,
            value=float(row["Business as Usual ($)"]),
            key=f"bau1_{row['id']}"
        )
        proposed = cols[2].number_input(
            "Proposed Tool ($)",
            min_value=0.0,
            step=10.0,
            value=float(row["Proposed Tool ($)"]),
            key=f"tool_{row['id']}"
        )
        notes = cols[3].text_input(
            "Notes",
            value=row["Notes"],
            key=f"notes_{row['id']}"
        )

        if cols[4].button("❌", key=f"del_cost_{row['id']}"):
            st.session_state.infrastructure_costs = [r for r in rows if r["id"] != row["id"]]
            st.rerun()

        # Update stored row
        row.update({
            "Cost Category": category,
            "Business as Usual ($)": BAU,
            "Proposed Tool ($)": proposed,
            "Notes": notes
        })

    # --- Add new row button ---
    if st.button("➕ Add Additional Cost Category"):
        st.session_state.infrastructure_costs.append({
            "id": str(uuid.uuid4()),
            "Cost Category": "",
            "Business as Usual ($)": 0.0,
            "Proposed Tool ($)": 0.0,
            "Notes": ""
        })
        st.rerun()

    # --- Convert to DataFrame ---
    df_infra = pd.DataFrame(st.session_state.infrastructure_costs).drop(columns="id")

    # --- Compute totals ---
    total_bau = df_infra["Business as Usual ($)"].sum()
    total_tool = df_infra["Proposed Tool ($)"].sum()

    # --- Add a Total row ---
    total_row = pd.DataFrame({
        "Cost Category": ["Total"],
        "Business as Usual ($)": [total_bau],
        "Proposed Tool ($)": [total_tool]
    })

    df_combined = pd.concat([df_infra, total_row], ignore_index=True)

    # --- Display combined table ---
    st.markdown("### Infrastructure Costs Table")
    st.dataframe(df_combined, use_container_width=True)

    # --- Store DataFrame for later use ---
    st.session_state.df_infrastructure_costs = df_combined
# =========================================================
#  OUTPUT PAGE
# =========================================================
elif page == "Project-Stage Efficiency Gains":
    st.header("📊 Project-Stage Efficiency Gains")

    # --- --- Helper function to compute total person-hours per stage ---
    def compute_total_time(df):
        """Compute total person-weeks per stage and convert to hours."""
        if df is None or df.empty:
            return pd.DataFrame(columns=["Stage", "Person-Hours"])
        df = df.copy()
        df["Total Duration (weeks)"] = pd.to_numeric(df.get("Total Duration (weeks)", 0), errors="coerce").fillna(0)
        df["Active Time Spent (%)"] = pd.to_numeric(df.get("Active Time Spent (%)", 0), errors="coerce").fillna(0)
        if "Stage" not in df.columns:
            df["Stage"] = "Unknown Stage"
        df["Person-Weeks"] = df["Total Duration (weeks)"] * df["Active Time Spent (%)"] / 100
        df_hours = df.groupby("Stage", as_index=False)["Person-Weeks"].sum()
        df_hours["Person-Hours"] = df_hours["Person-Weeks"] * 40
        return df_hours[["Stage", "Person-Hours"]]

    # --- Retrieve DataFrames ---
    df_bau1 = st.session_state.get("df_BAU", pd.DataFrame())
    df_tool = st.session_state.get("df_Proposed_Tool", pd.DataFrame())
    personnel_rows = st.session_state.get("personnel_rows", [])

    # --- Time Table ---
    df_time_bau1 = compute_total_time(df_bau1)
    df_time_tool = compute_total_time(df_tool)

    # Merge by Stage
    time_summary = pd.DataFrame({"Stage": project_stages})
    time_summary = time_summary.merge(df_time_bau1, on="Stage", how="left").rename(columns={"Person-Hours": "Business as Usual (hrs)"}).fillna(0)
    time_summary = time_summary.merge(df_time_tool, on="Stage", how="left").rename(columns={"Person-Hours": "Proposed Tool (hrs)"}).fillna(0)

    # Compute time saved
    time_summary["Time Saved vs BAU (hrs)"] = time_summary["Business as Usual (hrs)"] - time_summary["Proposed Tool (hrs)"]
    # Add totals row
    total_time_row = pd.DataFrame([{
        "Stage": "TOTAL",
        "Business as Usual (hrs)": time_summary["Business as Usual (hrs)"].sum(),
        "Proposed Tool (hrs)": time_summary["Proposed Tool (hrs)"].sum(),
        "Time Saved vs BAU (hrs)": time_summary["Time Saved vs BAU (hrs)"].sum()
    }])
    time_summary = pd.concat([time_summary, total_time_row], ignore_index=True)

    # --- Cost Table ---
    cost_summary = pd.DataFrame({"Stage": project_stages})

    for scenario in ["BAU", "Proposed_Tool"]:
        costs = []
        df_scenario = st.session_state.get(f"df_{scenario}", pd.DataFrame())
        for stage in project_stages:
            stage_rows = df_scenario[df_scenario["Stage"] == stage] if not df_scenario.empty else pd.DataFrame()
            stage_cost = 0
            for idx, row in stage_rows.iterrows():
                role = row.get("Role", "")
                pct_active = row.get("Active Time Spent (%)", 0)
                duration_weeks = row.get("Total Duration (weeks)", 0)
                # Look up hourly rate for this role
                hr_rate = next((p["Average Hourly Rate"] for p in personnel_rows if p["Role"] == role), 0)
                stage_cost += duration_weeks * pct_active / 100 * 40 * hr_rate
            costs.append(stage_cost)
        cost_summary[f"{scenario.replace('_',' ')} Cost ($)"] = costs

    # --- Add Infrastructure row ---
    infra_costs = st.session_state.get("df_infrastructure_costs", pd.DataFrame())
    if not infra_costs.empty:
        infra_row = {
            "Stage": "Infrastructure",
            "BAU Cost ($)": infra_costs.loc[infra_costs["Cost Category"]=="Total", "Business as Usual ($)"].values[0],
            "Proposed Tool Cost ($)": infra_costs.loc[infra_costs["Cost Category"]=="Total", "Proposed Tool ($)"].values[0]
        }
        cost_summary = pd.concat([cost_summary, pd.DataFrame([infra_row])], ignore_index=True)

    # --- Compute Cost Saved ---
    cost_summary["Cost Saved vs BAU ($)"] = cost_summary["BAU Cost ($)"] - cost_summary["Proposed Tool Cost ($)"]

    # --- Add TOTAL row ---
    total_row = pd.DataFrame([{
        "Stage": "TOTAL",
        "BAU Cost ($)": cost_summary["BAU Cost ($)"].sum(),
        "Proposed Tool Cost ($)": cost_summary["Proposed Tool Cost ($)"].sum(),
        "Cost Saved vs BAU ($)": cost_summary["Cost Saved vs BAU ($)"].sum()
    }])
    cost_summary = pd.concat([cost_summary, total_row], ignore_index=True)

    # --- Total Time Spent per Project Stage (ignoring personnel allocation) ---
    total_time_summary = pd.DataFrame({"Stage": project_stages})

    for scenario in ["BAU", "Proposed_Tool"]:
        durations = []
        df_scenario = st.session_state.get(f"df_{scenario}", pd.DataFrame())
        for stage in project_stages:
            stage_rows = df_scenario[df_scenario["Stage"] == stage] if not df_scenario.empty else pd.DataFrame()
            stage_time = 0
            if 'Step' in stage_rows.columns:
                for step in stage_rows["Step"].unique():
                    step_rows = stage_rows[stage_rows["Step"] == step]
                    stage_time += step_rows["Total Duration (weeks)"].max() if not step_rows.empty else 0
                durations.append(stage_time)  # Append after summing all steps in stage
            else:
                durations.append(stage_time)
        total_time_summary[f"{scenario.replace('_',' ')} Duration (weeks)"] = durations

    # Compute time saved (positive = time saved)
    total_time_summary["Time Saved vs BAU (weeks)"] = total_time_summary["BAU Duration (weeks)"] - total_time_summary["Proposed Tool Duration (weeks)"]

    # Add TOTAL row
    total_time_row = pd.DataFrame([{
        "Stage": "TOTAL",
        "BAU Duration (weeks)": total_time_summary["BAU Duration (weeks)"].sum(),
        "Proposed Tool Duration (weeks)": total_time_summary["Proposed Tool Duration (weeks)"].sum(),
        "Time Saved vs BAU (weeks)": total_time_summary["Time Saved vs BAU (weeks)"].sum()
    }])
    total_time_summary = pd.concat([total_time_summary, total_time_row], ignore_index=True)

    # --- Display tables ---
    st.info(""" 
            ### Duration (in weeks) by Project Stage ### 
            - This table presents the total duration per project stage (in weeks), ignoring personnel allocation and active time spent.
            - The **TOTAL** row provides the overall project-level duration. 
            """)
    st.dataframe(total_time_summary, use_container_width=True)

    st.info(""" 
            ### Active Person-Hours by Project Stage ###
            - This table presents the estimated total person-hours required for each stage of the research project across the **BAU** and **Proposed Tool** scenarios. 
            - **Time Saved** = hours saved by the Proposed Tool compared to BAU scenario (positive = less time required). 
            - All durations assume **40 working hours per week**. 
            - The **TOTAL** row provides the overall project-level summary. 
            """)

    st.dataframe(time_summary, use_container_width=True)

    st.info(""" 
            ### Cost by Project Stage ###
            - This table presents the estimated total personnel cost required for each stage of the research project as well as the non-personnel / infrastructure cost across the **BAU** and **Proposed Tool** scenarios. 
            - Personnel-cost is based on the % Active Time spent.
            - **Cost Saved** = hours saved by the Proposed Tool compared to BAU scenario (positive = less cost required). 
            - **Infrastructure** represents the total hardware / software cost (i.e. non personnel cost for the entire project)
            - The **TOTAL** row provides the overall project-level summary. 
            """)
    st.dataframe(cost_summary, use_container_width=True)

elif page == "Personnel Efficiency Gains":
    st.header("📊 Personnel Efficiency Gains")

    # Retrieve DataFrames
    df_bau1 = st.session_state.get("df_BAU_1", pd.DataFrame())
    df_bau2 = st.session_state.get("df_BAU_2", pd.DataFrame())
    df_tool = st.session_state.get("df_Proposed_Tool", pd.DataFrame())
    personnel_rows = st.session_state.get("personnel_rows", [])

    # Get unique roles
    roles = sorted({row.get("Role", "Unknown Role") for df in [df_bau1, df_bau2, df_tool] for _, row in df.iterrows()})

    # --- Person-Hours Table ---
    time_summary = pd.DataFrame({"Role": roles})
    for scenario_name, df_scenario in zip(["BAU", "Proposed Tool"], [df_bau1, df_bau2, df_tool]):
        hours_list = []
        for role in roles:
            role_rows = df_scenario[df_scenario["Role"] == role] if not df_scenario.empty else pd.DataFrame()
            total_hours = sum(
                row.get("Total Duration (weeks)", 0) * row.get("Active Time Spent (%)", 0) / 100 * 40
                for _, row in role_rows.iterrows()
            )
            hours_list.append(total_hours)
        time_summary[f"{scenario_name} (hrs)"] = hours_list

    # Compute time saved
    time_summary["Time Saved vs BAU (hrs)"] = time_summary["BAU (hrs)"] - time_summary["Proposed Tool (hrs)"]
    # Add TOTAL row
    total_time_row = pd.DataFrame([{
        "Role": "TOTAL",
        "BAU (hrs)": time_summary["BAU (hrs)"].sum(),
        "Proposed Tool (hrs)": time_summary["Proposed Tool (hrs)"].sum(),
        "Time Saved vs BAU (hrs)": time_summary["Time Saved vs BAU (hrs)"].sum()
    }])
    time_summary = pd.concat([time_summary, total_time_row], ignore_index=True)

    # --- Cost Table ---
    cost_summary = pd.DataFrame({"Role": roles})
    for scenario_name, df_scenario in zip(["BAU", "Proposed Tool"], [df_bau1, df_bau2, df_tool]):
        cost_list = []
        for role in roles:
            role_rows = df_scenario[df_scenario["Role"] == role] if not df_scenario.empty else pd.DataFrame()
            total_cost = 0
            for _, row in role_rows.iterrows():
                pct_active = row.get("Active Time Spent (%)", 0)
                duration_weeks = row.get("Total Duration (weeks)", 0)
                hr_rate = next((p["Average Hourly Rate"] for p in personnel_rows if p["Role"] == role), 0)
                total_cost += duration_weeks * pct_active / 100 * 40 * hr_rate
            cost_list.append(total_cost)
        cost_summary[f"{scenario_name} Cost ($)"] = cost_list

    # Compute cost saved
    cost_summary["Cost Saved vs BAU ($)"] = cost_summary["BAU Cost ($)"] - cost_summary["Proposed Tool Cost ($)"]

    # Add TOTAL row
    total_cost_row = pd.DataFrame([{
        "Role": "TOTAL",
        "BAU Cost ($)": cost_summary["BAU Cost ($)"].sum(),
        "Proposed Tool Cost ($)": cost_summary["Proposed Tool Cost ($)"].sum(),
        "Cost Saved vs BAU ($)": cost_summary["Cost Saved vs BAU ($)"].sum()
    }])
    cost_summary = pd.concat([cost_summary, total_cost_row], ignore_index=True)

    # --- Display ---
    st.info("""
        ### Active Person-Hours by Role
        - Shows total active hours per role across **BAU** and **Proposed Tool** scenarios.
        - **Time Saved** = hours saved by Proposed Tool compared to each BAU scenario (positive = less time required).
        - All durations assume 40 working hours per week.
        - The **TOTAL** row provides the overall summary across all roles.
        """)
    st.dataframe(time_summary, use_container_width=True)

    st.info("""
        ### Personnel Cost by Role
        - Shows total personnel cost per role across **BAU** and **Proposed Tool** scenarios.
        - Personnel-cost is based on the % Active Time spent.
        - Cost Saved = hours saved by the Proposed Tool compared to each BAU scenario (positive = less cost required).
        - The TOTAL row provides the overall project-level summary.
    """)
    st.dataframe(cost_summary, use_container_width=True)

elif page == "ROI":
    st.header("📈 Return on Investment (ROI) Analysis")
    st.markdown("#### Impact per Study")
    st.info(
        "Impact per Study is defined from the ROI Parameters as:\n\n"
        "***Discovery Rate*** × ***Per-student improvement in long-term economic opportunity*** × ***Total Reach*** "
        "(i.e., number of students impacted by the research study)"
    )
    # Retrieve total project durations in weeks
    total_time_summary = st.session_state.get("df_BAU_1", pd.DataFrame())
    durations_weeks = {}
    for scenario in ["BAU", "Proposed_Tool"]:
        df_scenario = st.session_state.get(f"df_{scenario}", pd.DataFrame())
        total_weeks = 0
        if not df_scenario.empty:
            total_weeks = df_scenario.groupby("Stage")["Total Duration (weeks)"].max().sum()
        durations_weeks[scenario] = total_weeks

    # Convert weeks to months (approx 4.345 weeks/month)
    durations_months = {k: v / 4.345 for k, v in durations_weeks.items()}

    # Retrieve total costs (personnel + infrastructure)
    cost_summary = st.session_state.get("df_infrastructure_costs", pd.DataFrame())
    total_costs = {}
    for scenario in ["BAU", "Proposed_Tool"]:
        # Sum infrastructure per-study cost
        infra_cost = 0
        if not cost_summary.empty:
            if scenario == 'BAU':
                infra_cost = cost_summary.loc[cost_summary["Cost Category"]=="Total", "Business as Usual ($)"].values[0]
            else:
                 infra_cost = cost_summary.loc[cost_summary["Cost Category"]=="Total", "Proposed Tool ($)"].values[0]
        # Add personnel cost
        df_scenario = st.session_state.get(f"df_{scenario}", pd.DataFrame())
        personnel_cost = 0
        personnel_rows = st.session_state.get("personnel_rows", [])
        for _, row in df_scenario.iterrows():
            role = row.get("Role","")
            pct_active = row.get("Active Time Spent (%)",0)
            duration_weeks = row.get("Total Duration (weeks)",0)
            hr_rate = next((p["Average Hourly Rate"] for p in personnel_rows if p["Role"]==role),0)
            personnel_cost += duration_weeks * pct_active / 100 * 40 * hr_rate
        total_costs[scenario] = personnel_cost + infra_cost

    # Compute Impact per study
    roi_params = st.session_state.get("roi_parameters", {})
    per_student_improvement = roi_params.get("computed_improvement", 0)
    evidence_rate = roi_params.get("evidence_rate", 0)/100
    total_students = roi_params.get("total_students", 0)

    impact_per_study = {}
    for scenario in ["BAU", "Proposed_Tool"]:
        impact_per_study[scenario] = per_student_improvement * evidence_rate * total_students

    # Build ROI DataFrame
    roi_df = pd.DataFrame({
        "Scenario": ["BAU", "Proposed Tool"],
        "Time (months)": [round(durations_months["BAU"],1),
                        round(durations_months["Proposed_Tool"],1)],
        "Cost ($)": [round(total_costs["BAU"],2),
                    round(total_costs["Proposed_Tool"],2)],
        "Impact per study ($)": [round(impact_per_study["BAU"],2),
                                round(impact_per_study["Proposed_Tool"],2)]
    })

    st.dataframe(roi_df, use_container_width=True)

    # Retrieve platform parameters
    roi_params = st.session_state.get("roi_parameters", {})
    num_orgs_bau1 = roi_params.get("orgs_bau1", 0)
    num_orgs_proposed = roi_params.get("orgs_proposed", 0)
    per_student_improvement = roi_params.get("computed_improvement", 0)
    evidence_rate = roi_params.get("evidence_rate", 0)/100
    total_students = roi_params.get("total_students", 0)
    total_investment = roi_params.get("total_investment", 0)
    num_concurrent_projects = roi_params.get("studies_proposed", 0)

    bau1_time = get_scenario_value("BAU", "Time (months)")
    tool_time = get_scenario_value("Proposed Tool", "Time (months)")

    bau1_cost = get_scenario_value("BAU", "Cost ($)")
    tool_cost = get_scenario_value("Proposed Tool", "Cost ($)")

    bau1_impact = get_scenario_value("BAU", "Impact per study ($)")
    tool_impact = get_scenario_value("Proposed Tool", "Impact per study ($)")

    # === User Inputs for Fixed Costs ===
    st.markdown('---')
    st.markdown("#### ⚙️ Adjust Fixed Costs (optional)")

    st.info("""
    - **Fixed Costs** — These are one-time or upfront expenses that do not change with the number of research studies conducted.  
    Examples include tool development, software setup, infrastructure installation, and initial onboarding or training.  
    This cost is **separate** from the operational cost of a research study (i.e., total personnel and infrastructure costs computed from your inputs).

    - **Variable Costs** — These are recurring or scalable expenses that increase with each additional research study.  
    Examples include data storage, API or tool usage, researcher time, or other per-study fees.  
    This cost is **derived directly** from the operational cost of the research study.
    """)

    col1, col2 = st.columns(2)
    with col1:
        fixed_bau1_user = st.number_input(
            "BAU Fixed Cost ($)", 
            value=0,
            help='The fixed cost in the Business as Usual (BAU) scenario is set to 0 by default, as it assumes the organization is establishing its research process for the first time. If a custom tool or off-the-shelf solution is being used, it is assumed that each new research study incurs the same setup cost. In reality, however, once initial operations are established, these costs tend to decrease over time. Therefore, you may adjust the fixed cost to better reflect actual long-term efficiencies.')
    with col2:
        fixed_tool_user = st.number_input(
            "Proposed Tool Fixed Cost ($)",
            value=total_investment,
            help="The fixed cost in the Proposed Tool scenario represents the grantee organization's investment in developing or implementing the tool, as this is assumed to be the amount required for initial setup. This value can be adjusted as needed to reflect actual or projected costs.")

    # === Charts ===
    st.markdown('---')
    st.markdown("### 📉 Impact per Dollar Over Time")

    projection_data = []

    # Compute projections for each scenario
    projection_data_bau1 = compute_projection("BAU", bau1_time, bau1_cost, bau1_impact, fixed_bau1_user, num_orgs_bau1, num_concurrent_projects)
    projection_data_pt = compute_projection("Proposed Tool", tool_time, tool_cost, tool_impact, fixed_tool_user, num_orgs_proposed, num_concurrent_projects)

    # Convert to DataFrame
    roi_projection_all = pd.DataFrame(projection_data_bau1)

    fig1 = px.line(
        roi_projection_all,
        x="Year",
        y="Impact per $ (Variable only)",
        color="Scenario",
        title="Impact per Dollar (Variable Cost Only for Proposed Tool)",
        markers=True
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Chart 2: Include Fixed + Variable Costs for all
    fig2 = px.line(
        roi_projection_all,
        x="Year",
        y="Impact per $ (Total cost)",
        color="Scenario",
        title="Impact per Dollar (Including Fixed + Variable Costs)",
        markers=True
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("##### ROI Data Table")
    st.dataframe(roi_projection_all, use_container_width=True)

# =========================================================
#  FIXED NAVIGATION BUTTONS
# =========================================================
current_idx = PAGES.index(page)
placeholder = st.empty()

with placeholder.container():
    st.markdown("<div class='nav-buttons'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        if current_idx > 0:
            if st.button("⬅️ Back", key="back"):
                go_back()
                st.rerun()

    with col3:
        if current_idx < len(PAGES) - 1:
            if st.button("Next ➡️", key="next"):
                go_next()
                st.rerun()
        elif current_idx == len(PAGES) - 1:
            if st.button("🔁 Reset", key="restart"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                go_first()
                st.rerun()  # Reloads the app from the top