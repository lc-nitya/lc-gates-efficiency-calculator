import streamlit as st
import pandas as pd
import uuid
import math
import plotly.express as px

# --- Page configuration ---
st.set_page_config(
    page_title="Efficiency Gains Calculator and Social ROI Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"  # Keep sidebar open
)

# --- Define pages and hierarchy ---
PAGE_GROUPS = {
    "Instructions": [],
    "Inputs": {
        "Personnel Costs": [],
        "Infrastructure Costs": [],
        "Social ROI Parameters": [],
        "Project Activities": ["Business as Usual", "Proposed Tool"],
    },
    "Outputs": {
        "Project-Stage Efficiency Gains": [],
        "Personnel Efficiency Gains": [],
        "Social ROI": []
    }
}

# Flatten pages for sequential navigation
PAGES = [
    "Instructions",
    "Personnel Costs",
    "Infrastructure Costs",
    "Social ROI Parameters",
    "Business as Usual",
    "Proposed Tool",
    "Project-Stage Efficiency Gains",
    "Personnel Efficiency Gains",
    "Social ROI"
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
        st.sidebar.markdown(f"**{page_name}**")
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
        {"id": str(uuid.uuid4()), "Role": "Engineer", "Hourly Rate": 0.0,
         "Notes": ""},
        {"id": str(uuid.uuid4()), "Role": "Researcher", "Hourly Rate": 0.0, "Notes": ""},
        {"id": str(uuid.uuid4()), "Role": "Project Manager", "Hourly Rate": 0.0,
         "Notes": ""},
    ]
personnel_roles = [p["Role"] for p in st.session_state.personnel_rows]

# --- Project stages ---
project_stages = [
    "Data Agreements & Research Approvals",
    "Data Collection & Access or Transfer",
    "Study Design & Infrastructure Setup",
    "Study Implementation & Monitoring",
    "Data Modeling & Analysis",
    "Reporting"
]


# --- Helper function to render project activity sections ---
def render_activity_section(section_name):
    """
    Renders the project activity section in Streamlit.

    Args:
        section_name (str): The name of the project activity section.

    Actions:
    For each stage in the project, this function:
        - Initializes default steps if none exist
        - Displays an expander for each stage
        - Allows editing of step description, notes, duration, and role-based active time
        - Provides buttons to add or delete steps
        - Collects all data into a consolidated preview table
    """

    # List to collect all preview data
    all_preview_data = []
    st.markdown("#### Project Stages ####")
    for stage in project_stages:
        with st.expander(stage, expanded=False):
            # Initialize stage in session_state if empty
            if stage not in st.session_state.project_steps[section_name]:
                st.session_state.project_steps[section_name][stage] = []

                # Prefill stage-specific steps
                if stage == 'Data Agreements & Research Approvals':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Drafting agreements, review, executing DSAs and DUAs",
                            "Notes": "",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        },
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
                            "Notes": ("e.g. Obtaining consent from users / students using the curriculum "
                                      "platform through ToS, pop-up or checkbox, or another form of notification"),
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                elif stage == 'Data Collection & Access or Transfer':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Data Collection, Documentation, Anonymization (Data setup)",
                            "Notes": ("e.g. Collecting individual observations, querying, verification, "
                                      "troubleshooting, anonymization, and documentation"),
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        },
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Secure data access / transfer to researchers",
                            "Notes": ("e.g. District may share data via secure file storage. Requires account setup, "
                                      "permissions, VPN configuration, and validation."),
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                elif stage == 'Study Design & Infrastructure Setup':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Data Prep and Exploration",
                            "Notes": ("e.g. Review, clean, merge, validate datasets; run power calculations, "
                                      "determine randomization strategy."),
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        },
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Data preparation to implement the study",
                            "Notes": ("e.g. Prepare content or implement feature changes for A/B testing: "
                                      "update database, UI, variants."),
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        },
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Infrastructure setup for experiment execution",
                            "Notes": ("e.g. Setup database, pipelines, dashboards, integrate content, QA, "
                                      "documentation, training."),
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                elif stage == 'Study Implementation & Monitoring':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Run the study",
                            "Notes": ("e.g. Run pilot study, scale, monitor, and share periodic data."),
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                elif stage == 'Data Modeling & Analysis':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Analysis & QA",
                            "Notes": ("e.g. Verify experiment, run statistical/ML analyses, interpret findings, "
                                      "produce descriptives/graphs."),
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                elif stage == 'Reporting':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Report writing & communications",
                            "Notes": (
                                "e.g. Setup dashboards, publish reports, disseminate findings, propose next steps."),
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                else:
                    # Default empty step
                    st.session_state.project_steps[section_name][stage] = [{
                        "id": str(uuid.uuid4()),
                        "Step": "",
                        "Notes": "",
                        "Duration": 0.0,
                        "Roles": {r: 0.0 for r in personnel_roles}
                    }]

            # --- Render all rows for the current stage ---
            rows = st.session_state.project_steps[section_name][stage]

            for idx, row in enumerate(rows.copy()):
                st.markdown(f"<span style='color:#DF7861; font-weight:bold;'>**Step {idx + 1}**</span>",
                            unsafe_allow_html=True)

                # Step Description and Notes
                cols1 = st.columns([4, 4])
                row["Step"] = cols1[0].text_area("Step Description", value=row.get("Step", ""),
                                                 key=f"{section_name}_{stage}_step_{row['id']}", height=80)
                row["Notes"] = cols1[1].text_area("Notes", value=row.get("Notes", ""),
                                                  key=f"{section_name}_{stage}_notes_{row['id']}", height=80)

                # Duration
                cols2 = st.columns([2])
                row["Duration"] = cols2[0].number_input(
                    "Total Duration (weeks)",
                    min_value=0.0,
                    step=1.0,
                    format="%.2f",
                    value=row.get("Duration", 0.0),
                    key=f"{section_name}_{stage}_dur_{row['id']}"
                )

                # Active time per role
                st.markdown(f"<span style='color:#ECB390;'>*% Active Time Spent per Role*</span>",
                            unsafe_allow_html=True)
                time_data = {}
                roles_per_row = 5
                for i in range(0, len(personnel_roles), roles_per_row):
                    role_subset = personnel_roles[i:i + roles_per_row]
                    cols = st.columns(roles_per_row)
                    for j, role in enumerate(role_subset):
                        with cols[j]:
                            time_data[role] = st.number_input(
                                role,
                                min_value=0.0,
                                step=1.0,
                                value=row.get("Roles", {}).get(role, 0.0),
                                format="%.2f",
                                key=f"{section_name}_{stage}_{role}_{row['id']}"
                            )
                    # Fill remaining columns for layout
                    for j in range(len(role_subset), roles_per_row):
                        with cols[j]:
                            st.markdown("")

                row["Roles"] = time_data

                # Delete step button
                if st.button("❌ Delete", key=f"del_{section_name}_{stage}_{row['id']}"):
                    st.session_state.project_steps[section_name][stage] = [
                        r for r in rows if r["id"] != row["id"]
                    ]
                    st.rerun()

                st.markdown("---")

            # Add new step button
            if st.button(f"➕ Add Step to {stage}", key=f"add_{section_name}_{stage}"):
                st.session_state.project_steps[section_name][stage].append({
                    "id": str(uuid.uuid4()),
                    "Step": "",
                    "Notes": "",
                    "Duration": 0.0,
                    "Roles": {r: 0.0 for r in personnel_roles}
                })
                st.rerun()

            # Collect all stage data for final preview
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

    # --- Render final consolidated preview table ---
    if all_preview_data:
        st.markdown(f"#### {section_name} Activities Table ####")
        df = pd.DataFrame(all_preview_data)
        st.dataframe(df, use_container_width=True)

        # Save final table in session_state for computations
        st.session_state[f"df_{section_name.replace(' ', '_')}"] = df


# --- Helper function to copy all project activities from BAU to proposed tool (on button click)---
def copy_from_section(source_section, target_section):
    """
    Copy all project steps from a source section to a target section.

    Each step in the target section receives a **new UUID**, while preserving
    Step description, Notes, Duration, and Roles.

    Args:
        source_section (str): Name of the section to copy from.
        target_section (str): Name of the section to copy to.

    Actions:
        - Overwrites any existing steps in the target section.
        - Provides a success message if copy is successful.
        - Warns if the source section has no data.
    """
    if source_section in st.session_state.project_steps:
        # Initialize target section as empty
        st.session_state.project_steps[target_section] = {}

        # Copy each stage and its steps
        for stage, steps in st.session_state.project_steps[source_section].items():
            copied_steps = []
            for step in steps:
                copied_steps.append({
                    "id": str(uuid.uuid4()),  # Assign a new unique ID
                    "Step": step["Step"],
                    "Notes": step["Notes"],
                    "Duration": step["Duration"],
                    "Roles": step["Roles"].copy()  # Ensure roles dictionary is copied
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

    Args:
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
    """
    Retrieve a specific value from the ROI dataframe for a given scenario.

    Args:
        scenario (str): The name of the scenario to look up in the "Scenario" column of `roi_df`.
        col (str): The name of the column from which to retrieve the value.

    Returns:
        The value from the specified column for the matching scenario.
        Returns 0 if the scenario or column is not found, or if any error occurs.
    """
    try:
        return roi_df.loc[roi_df["Scenario"] == scenario, col].values[0]
    except:
        return 0


# --- Main Page ---
st.title("Efficiency Gains Calculator and Social ROI Dashboard")
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
            This tool was originally developed to help the Gates Foundation benchmark efficiency gains from its research and development (R&D) infrastructure investment portfolio. These investments aimed to make education research faster, more cost-effective and more scalable. 
            
            This tool presents a framework to estimate potential efficiency gains–defined as time and cost savings–and the broader social return on investment (ROI) from conducting research more efficiently. By quantifying how infrastructure accelerates research, the tool helps illustrate the value of building systems that allow researchers to test more ideas, more often. This framework can be used by funders, investors, researchers and ed tech organizations seeking to quantify and communicate the efficiency gains created by their own tools or infrastructure.  

            #### Goals ####
            
            **This tool was developed to provide a consistent, evidence-based framework for understanding how investments in R&D.**
            - **Establish a standardized framework** for calculating efficiency gains across organizations.
            - **Enable data-driven comparisons** between current research processes and those improved by the proposed or new R&D infrastructure..
            - **Generate  clear, evidence-based insights** to help both funders, investors and organizations understand the ROI and long-term impact of their investments.
            
            We believe this tool can be useful for many kinds of organizations — philanthropies, investors, and tech organizations (both for-profit and nonprofit) — helping them better understand, amplify, and communicate the impact of their work.
            """)

    st.markdown("---")
    st.markdown("## 🧰   Example Use Cases")
    st.markdown("---")

    st.markdown("""
    1. **Foundation Program Officer** - If you're a program officer looking to measure the long-term social returns of your investments — say, in improving middle school math outcomes — this tool can help you predict those returns with evidence. You can also share the link with your portfolio partners to collect data on cost and time savings, as well as overall ROI.
    2. **Impact-Driven Organization** - If you're a founder or strategist wondering whether investing in a new technology will actually save time and money, the Efficiency Gains Calculator can show you the data. It even breaks down where those savings happen — across different research phases or team roles — so you can see exactly where the biggest gains are. You can edit or replace different research phases with stages that are relevant for your use case. 
    3. **EdTech Founder** - If you're building an education-focused product or intervention, this tool can give you evidence to strengthen your fundraising case. It helps you estimate the potential long-term economic benefits your solution could create.
    4. **Education Researcher** - If you're a researcher proposing new technology to improve education R&D, you can use this tool to quickly see how your idea might change current processes — in terms of time, cost, and social returns. It provides a fast, standardized way to translate innovation into measurable outcomes. 
    5. **Team Leader or Project Manager** - If you're managing a research or product team, the calculator can also be used to model how changes in personnel impact efficiency. For example, adding data engineers or research assistants may reduce bottlenecks in setup and analysis, helping you test whether increasing personnel capacity leads to greater overall time and cost savings. """)

    st.markdown("---")
    st.markdown("## ⚙️ Our Approach")
    st.markdown("---")

    st.subheader("Efficiency Gains Calculator")
    st.markdown("""
    ***Efficiency*** is defined as the time and cost required to generate high-quality evidence about what works. This calculator applies the Ingredient Method (Levin et al, 2017), a cost analysis approach that breaks down research activities into their core inputs, or “ingredients”, such as personnel and infrastructure. 
    To use the framework, outline the key research activities involved at different stages of your process (e.g. study design, implementation, analysis) and estimate the time and cost associated with each stage. Then, compare how those activities look under two conditions:
    
    - **Business-as-Usual (BAU)**: How research is conducted today, without the new tool or infrastructure. 
    - **Proposed Tool or Intervention**: How research is conducted after adopting your new infrastructure, tool or process. 
    
    The calculator aggregates these inputs to estimate time and cost savings across stages, roles and activities. 
    
    *Note*: It's possible that you find estimating the exact time challenging - please note this is an exercise in estimation and generalization, not precision. Even approximate estimates provide valuable insight into where efficiency gains occur. It might be helpful to make explicit assumptions for your before and after inputs. Please remember thoughtful approximations are better than blanks.
    """)

    st.subheader("Social ROI (Return on Investment) Calculator")

    st.markdown("""
    This section presents a framework for estimating the Social Return on Investment (ROI) 
    from R&D infrastructure in education. We link the social benefits of faster, cheaper research 
    to the impact of studies that show gains in middle school math performance.
    
    **Key Metrics**
    - **Typical Effect Sizes**: Median impacts in math range from 0.04 to 0.09 SD, with a median of 0.12 SD (Kraft, 2019).
    - **Long-term Earnings Impact**: A 0.5 SD gain in math scores during middle school increases adult earnings by 3.5% 
    (approx \$1,200 per year in 2018, Urban Institute, 2024). A 0.12 SD gain translates to \$288 per year in additional earnings per student at age 30. These effects are similar across race and ethnicity.
    - **Discovery Rate**: According to the Good Science Project we only have about a 10% success rate in identifying effective interventions.
    
    **ROI Calculation**
    ROI is based on the number of studies, the probability of positive findings (discovery rate), and the observed impact on math scores and future earnings, scaled by the number of students using the platform through which research findings are implemented.
    
    **Notes on returns**
    - **Scalability drives ROI**: In our ROI framework, returns from R&D infrastructure depend on translating discoveries into implementation. As a reference point for scale, use the number of students/users you think would be impacted by your product/intervention. This can be the number of users who use your product/intervention. 
    - **Sequential studies**: In our framework, we assume that only one study is conducted at a time across all scenarios i.e. business-as-usual and under the proposed tool or infrastructure. This assumption is made solely to keep the model conservative and straightforward, allowing us to estimate the minimum ROI that could be observed from these investments. 
    - **Fixed cost**: Fixed cost is equal to the initial investment of building a tool/infrastructure. 
    - **Variable cost**: This is the cost associated to different research stages under the new proposed tool/infrastructure
    - **Cost calculation**: Costs include both completed and in-progress studies
    """)

    st.markdown("---")
    st.markdown("## 📝️  Instructions")
    st.markdown("---")

    st.subheader("Before you begin")
    st.markdown("""
    - Before getting started, make sure you have a clear understanding of the types of research projects your proposed tool supports.
        - For example, if you're developing an A/B testing platform to evaluate ed-tech interventions, a relevant research project might involve testing student performance on math questions with and without AI-generated hints.
    - Consider all the key roles involved in implementing such a study, such as data engineers, data scientists, project managers, and research leads.
    - Also consider the key steps in conducting the research, including tasks like establishing data-sharing agreements, obtaining student consent, managing data storage and security, random sampling, conducting analysis, and writing and disseminating the final report.
    - Finally, think about which steps in the research process - and which roles involved - your proposed tool helps make more efficient, and how it does so. Consider the specific challenges your tool aims to solve, such as reducing manual effort, improving data accessibility, streamlining collaboration, or accelerating analysis and reporting.
    - This tool guides you through the process by comparing how a research project operates today (**Business as Usual** Scenario) versus how it would function with the tool in place (**Proposed Tool** Scenario).""")

    st.subheader("Steps")
    st.markdown("""
    1. **Use the Sidebar** to navigate between pages.  
    2. **Enter the Input Data**
        - **Personnel Costs**: Specify the roles/personnel and salaries involved in conducting the research project
        - **Infrastructure Costs**: Specify the non-personnel cost (e.g. hardware, software, storage, API usage) required 
        to conduct the research project in both **Business as Usual** and **Proposed Tool** scenarios.
        - **Social ROI Parameters**: Fill in the relevant metrics to conduct an ROI analysis for both scenarios (e.g. Number of 
        organizations conducting research that are supported concurrently, Total investment by grantees, Estimated impact of a single research project)
    3. **Project Activities**
        - **Business as Usual**: Consider how the research project would run **without** the proposed tool. 
        For each stage of the project, describe the steps involved and estimate the total time and personnel effort required. 
        If a stage doesn't apply, you can leave it blank.
        - **Proposed Tool**: Consider how the research project would run **with** the proposed tool. 
        For each stage of the project, describe the steps involved and estimate the total time and personnel effort required. 
        If a stage doesn't apply, you can leave it blank. To simplify, you can **copy estimates from the Business as Usual scenario** and make edits only for the stages where the proposed tool is expected to change time or personnel effort.
    4. **View Outputs**
        - **Project-Stage Efficiency Gains**: Time and cost savings for a single research project using the proposed tool, 
        broken down by research project stage. These values are automatically calculated based on input data.
        - **Personnel Efficiency Gains**:  Time and cost savings for a single research project using the proposed tool, 
        broken down by personnel/roles involved. These values are automatically calculated based on input data.
        - **Social ROI**: Return on investment for grantee organizations, scaled by the estimated number of 
        organizations supported in the Business as Usual vs. Proposed Tool scenarios.
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
            {"id": str(uuid.uuid4()), "Role": "Engineer", "Hourly Rate": 65.0,
             "Notes": "e.g. Software or Data Engineer"},
            {"id": str(uuid.uuid4()), "Role": "Researcher", "Hourly Rate": 25.0, "Notes": "e.g. PhD student"},
            {"id": str(uuid.uuid4()), "Role": "Project Manager", "Hourly Rate": 48.0,
             "Notes": "e.g. Partnerships or research manager"},
        ]

    rows = st.session_state.personnel_rows

    for idx, row in enumerate(rows):
        # Ensure all keys exist in case of malformed rows
        row.setdefault("id", str(uuid.uuid4()))
        row.setdefault("Role", "")
        row.setdefault("Hourly Rate", 0.0)
        row.setdefault("Notes", "")

        st.markdown(f"<span style='color:#DF7861'>***Personnel {idx + 1}***</span>", unsafe_allow_html=True)

        cols = st.columns([4, 3, 7, 1])  # Narrow column for trash icon

        # Editable inputs
        role = cols[0].text_input("Role", row["Role"], key=f"role_{row['id']}")
        rate = cols[1].number_input("Hourly Rate ($)", min_value=0.0,
                                    value=row["Hourly Rate"],
                                    step=1.0,
                                    key=f"rate_{row['id']}")
        notes = cols[2].text_input("Notes", row["Notes"], key=f"notes_{row['id']}")

        # Delete button
        if cols[3].button("❌", key=f"del_{row['id']}"):
            st.session_state.personnel_rows = [r for r in rows if r["id"] != row["id"]]
            st.rerun()

        # Update row in session state
        row.update({"Role": role, "Hourly Rate": rate, "Notes": notes})

    # Add new row
    if st.button("➕ Add Row"):
        st.session_state.personnel_rows.append({
            "id": str(uuid.uuid4()), "Role": "", "Hourly Rate": 0.0, "Notes": ""
        })
        st.rerun()

    # Display summary
    st.write("#### Personnel Costs Table")
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
        "Overall project stage titles are not editable to serve as consistent framework across projects."
        "The steps listed under each project stage are intended as a guiding framework to help you complete this "
        "section. You may edit, add, or delete the steps under each project stage so that they align with the types "
        "of projects your tool supports. "
        "Please note: deleting a step means it is not required to complete the research project. Even if your "
        "proposed tool does not target a particular step, the step must be included if it is relevant to conducting "
        "the research project. "
        "You may include any additional notes related to the execution of each project step. This is particularly "
        "useful in the ***Proposed Tool*** scenario to explain why a step shows a significant difference in total "
        "time or personnel effort compared to ***Business as Usual***. "
    )
    render_activity_section("BAU")

elif page == "Proposed Tool":
    st.markdown("---")
    st.header("📊 Project Activities: *Proposed Tool*")
    st.markdown("---")
    st.caption(
        "Overall project stage titles are not editable to serve as consistent framework across projects."
        "The steps listed under each project stage are intended as a guiding framework to help you complete this "
        "section. You may edit, add, or delete the steps under each project stage so that they align with the types "
        "of projects your tool supports. "
        "Please note: deleting a step means it is not required to complete the research project. Even if your "
        "proposed tool does not target a particular step, the step must be included if it is relevant to conducting "
        "the research project. "
        "You may include any additional notes related to the execution of each project step. This is particularly "
        "useful in the ***Proposed Tool*** scenario to explain why a step shows a significant difference in total "
        "time or personnel effort compared to ***Business as Usual***. "
    )

    # --- Collapsible section using expander ---
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📋 Pre-Fill estimates from Business as Usual"):
        st.markdown(
            "Save time by copying all estimates from the Business as Usual scenario. You can then adjust estimates "
            "where the proposed tool changes things.")
        st.warning(
            "⚠️Any edits you've made on this page will be overwritten if you select 'Yes'"
        )

        # Radio buttons: default is No
        choice = st.radio(
            "Do you want to proceed?",
            options=["No", "Yes"],
            index=0  # default to "No"
        )

        # Act only if user selects Yes
        if choice == "Yes":
            copy_from_section("BAU", "Proposed Tool")
    st.markdown("---")

    render_activity_section("Proposed Tool")

# =========================================================
#  ROI PARAMETERS PAGE
# =========================================================
elif page == "Social ROI Parameters":
    st.markdown("---")
    st.header("📈 Social ROI Parameters")
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
            help='Specify estimated median impact in standard deviations. See info below for typical ranges.'
        )

    st.caption("""
    **Note on Typical Impact / Effect Sizes:**  
    Median impacts in math range from 0.04 to 0.09 SD, with a median of 0.12 SD (Kraft, 2019).  
    This number is only a reference point. You can adjust the impact size per the actual results of your research studies.
    """)

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
            help="Enter the expected average increase in the long-term economic opportunity outcome for a 1 standard "
                 "deviation improvement in the primary outcome",
            key="roi_econ_per_sd"
        )

    # Add spacing after
    st.write("")

    # --- Per-Student Outcome Improvement (Computed) ---
    computed_improvement = learning_sd * econ_per_sd
    st.number_input("Per-student improvement in long-term economic opportunity (in $)", value=computed_improvement,
                    disabled=True)

    st.caption("""
    **Note on Long-term Economic Opportunity (or Earnings Impact):**  
    A 0.5 SD gain in math scores during middle school increases adult earnings by 3.5% (approx. \$1,200 per year in 2018, Urban Institute, 2024).
    A 0.12 SD gain (i.e. median impact) translates to \$288 per year in additional earnings per student at age 30.
    These effects are similar across race and ethnicity. 
    
    You can adjust the above number for inflation using this link: https://www.bls.gov/data/inflation_calculator.htm """)

    # --- Evidence Generation ---
    st.markdown("<h3 style='color:#ECB390;'>Discovery Rate</h3>", unsafe_allow_html=True)
    discovery_rate = st.number_input(
        "Rate of discovery of impact (%)",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=1.0,
        format="%.2f",
        key="roi_discovery_rate",
        help="The estimated probability that a research project will detect measurable impact in the primary outcome"
    )

    st.caption(
        '**Note on Discovery Rate**: According to the Good Science Project we only have about a 10% success rate in '
        'identifying effective interventions.')

    # --- Research Study Reach & Investment ---
    st.markdown("<h3 style='color:#ECB390;'>Reach and Impact</h3>", unsafe_allow_html=True)
    st.caption("You can explore different scenarios by adjusting the inputs based on your assumptions.")
    col1, col2 = st.columns(2)
    with col1:
        total_students = st.number_input(
            "Total reach of the research study (# individuals impacted).",
            min_value=1,
            step=1,
            key="roi_total_students",
            help="Enter the total number of individuals affected by the research project. E.g., the number of "
                 "students on the ed-tech platform that implements a research intervention. "
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
        orgs_bau = st.number_input(
            "Orgs supported (Business as Usual)",
            min_value=1,
            step=1,
            value=1,
            key="roi_orgs_bau",
            help=(
                """
                Specify the number of organizations that can use the solution in the Business as Usual scenario.
                Only relevant when the tool or infrastructure impacts more than one organization; otherwise, the default is 1.
                
                The total number of concurrent projects depends on:
                - The number of organizations using the solution (BAU or proposed tool).
                - The number of projects each organization can run concurrently."""
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
                """
                Specify the number of organizations that can use the solution in the Proposed Tool scenario.
                Only relevant when the tool or infrastructure impacts more than one organization; otherwise, the default is 1.

                The total number of concurrent projects depends on:
                - The number of organizations using the solution (BAU or proposed tool).
                - The number of projects each organization can run concurrently."""
            )
        )

    with col3:
        concurrent_studies = st.number_input(
            "Concurrent research projects per org",
            min_value=1,
            value=1,
            step=1,
            key="roi_concurrent_studies",
            help=(
                """
                Specify how many research studies each organization can run at the same time using the solution.
                The default value of 1 is used to keep the model conservative and straightforward, providing an estimate of the minimum ROI.
    
                The total number of concurrent projects depends on:
                - The number of organizations using the solution (BAU or proposed tool).
                - The number of projects each organization can run concurrently."""
            )
        )

    # --- Save all ROI parameters in session_state for later use ---
    st.session_state.roi_parameters = {
        "learning_definition": learning_definition,
        "learning_sd": learning_sd,
        "econ_definition": econ_definition,
        "econ_per_sd": econ_per_sd,
        "computed_improvement": computed_improvement,
        "discovery_rate": discovery_rate,
        "total_students": total_students,
        "total_investment": total_investment,
        "orgs_proposed": orgs_proposed,
        "orgs_bau": orgs_bau,
        "concurrent_studies": concurrent_studies
    }

# =========================================================
#  ASSUMPTIONS PAGES -- currently excluded
# =========================================================
elif page == "Assumptions":
    st.markdown("---")
    st.header("🧩 Assumptions")
    st.markdown("---")

    st.caption("List any assumptions made during your analysis below. "
               "You can add multiple entries, edit or delete them, and download the full list as a CSV file. This "
               "list is for your reference only, it is not used in any calculations.")

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
        """
        Enter the per-study **infrastructure costs** (e.g., hardware, software, storage, API usage) for both the 
        Business as Usual and Proposed Tool scenarios. These are non-personnel operational costs. While organizations 
        typically pay for subscriptions or services shared across multiple research projects, please provide your 
        best estimate for **per-study costs**. 
        
        The cost categories listed below serve as a guiding framework. You may edit, add, or delete categories,
        adjust amounts, and add notes as needed.
        
        The estimates represent the **total infrastructure cost** from the perspective of a single end user — i.e.,
        an organization conducting research supported by the proposed tool. """
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
            key=f"bau_{row['id']}"
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
    st.markdown("#### Infrastructure Costs Table ####")
    st.dataframe(df_combined, use_container_width=True)

    # --- Store DataFrame for later use ---
    st.session_state.df_infrastructure_costs = df_combined

# =========================================================
#  OUTPUT PAGE
# =========================================================
elif page == "Project-Stage Efficiency Gains":
    st.header("📊 Project-Stage Efficiency Gains")


    # --- Helper function to compute total person-hours per stage ---
    def compute_total_time(df):
        """
        Compute total person-hours per stage from a dataframe of activity estimates.

        Args:
            df (pd.DataFrame): A dataframe containing the following columns:
                - "Stage": Name of the project stage.
                - "Total Duration (weeks)": Duration of the step in weeks.
                - "Active Time Spent (%)": Percent of time each role spends on the step.

        Returns:
            pd.DataFrame: A dataframe with columns:
                - "Stage": Project stage.
                - "Person-Hours": Total hours spent by all roles for that stage.
        """
        # Return empty dataframe if input is None or empty
        if df is None or df.empty:
            return pd.DataFrame(columns=["Stage", "Person-Hours"])

        df = df.copy()

        # Ensure numeric values and fill missing/invalid data with 0
        df["Total Duration (weeks)"] = pd.to_numeric(df.get("Total Duration (weeks)", 0), errors="coerce").fillna(0)
        df["Active Time Spent (%)"] = pd.to_numeric(df.get("Active Time Spent (%)", 0), errors="coerce").fillna(0)

        # Fill missing Stage column
        if "Stage" not in df.columns:
            df["Stage"] = "Unknown Stage"

        # Compute Person-Weeks per row
        df["Person-Weeks"] = df["Total Duration (weeks)"] * df["Active Time Spent (%)"] / 100

        # Aggregate Person-Weeks by Stage
        df_hours = df.groupby("Stage", as_index=False)["Person-Weeks"].sum()

        # Convert Person-Weeks to Person-Hours (assuming 40-hr weeks)
        df_hours["Person-Hours"] = df_hours["Person-Weeks"] * 40

        # Return only relevant columns
        return df_hours[["Stage", "Person-Hours"]]


    # ------------------------------------------
    # --- Total Time Spent per Project Stage ---
    # ------------------------------------------
    # --- Retrieve DataFrames ---
    df_bau = st.session_state.get("df_BAU", pd.DataFrame())
    df_tool = st.session_state.get("df_Proposed_Tool", pd.DataFrame())
    personnel_rows = st.session_state.get("personnel_rows", [])

    # --- Compute Time Tables for BAU and Proposed Tool ---
    df_time_bau = compute_total_time(df_bau)  # Total person-hours per stage for Business as Usual
    df_time_tool = compute_total_time(df_tool)  # Total person-hours per stage for Proposed Tool

    # --- Merge time tables by Stage ---
    time_summary = pd.DataFrame({"Stage": project_stages})  # Start with all project stages

    # Merge BAU data
    time_summary = (
        time_summary
        .merge(df_time_bau, on="Stage", how="left")  # Merge BAU hours
        .rename(columns={"Person-Hours": "Business as Usual (hrs)"})  # Rename column
        .fillna(0)  # Fill missing stages with 0
    )

    # Merge Proposed Tool data
    time_summary = (
        time_summary
        .merge(df_time_tool, on="Stage", how="left")  # Merge tool hours
        .rename(columns={"Person-Hours": "Proposed Tool (hrs)"})  # Rename column
        .fillna(0)  # Fill missing stages with 0
    )

    # --- Compute Time Saved vs BAU ---
    time_summary["Time Saved vs BAU (hrs)"] = (
            time_summary["Business as Usual (hrs)"] - time_summary["Proposed Tool (hrs)"]
    )

    # --- Add Total row ---
    total_time_row = pd.DataFrame([{
        "Stage": "Total",
        "Business as Usual (hrs)": time_summary["Business as Usual (hrs)"].sum(),
        "Proposed Tool (hrs)": time_summary["Proposed Tool (hrs)"].sum(),
        "Time Saved vs BAU (hrs)": time_summary["Time Saved vs BAU (hrs)"].sum()
    }])

    # Append total row to the summary
    time_summary = pd.concat([time_summary, total_time_row], ignore_index=True)

    # --------------------------------------------------------------------------
    # --- Total Time Spent per Project Stage (ignoring personnel allocation) ---
    # --------------------------------------------------------------------------
    total_time_summary = pd.DataFrame({"Stage": project_stages})  # Initialize summary with project stages

    # Loop through each scenario: Business as Usual (BAU) and Proposed Tool
    for scenario in ["BAU", "Proposed_Tool"]:
        durations = []

        # Get the scenario-specific dataframe from session state; default to empty
        df_scenario = st.session_state.get(f"df_{scenario}", pd.DataFrame())

        # Loop through each stage
        for stage in project_stages:
            # Filter rows corresponding to the current stage
            stage_rows = df_scenario[df_scenario["Stage"] == stage] if not df_scenario.empty else pd.DataFrame()

            stage_time = 0  # Initialize stage time accumulator

            # Sum the maximum duration for each unique step within the stage
            if "Step" in stage_rows.columns:
                for step in stage_rows["Step"].unique():
                    step_rows = stage_rows[stage_rows["Step"] == step]
                    if not step_rows.empty:
                        stage_time += step_rows["Total Duration (weeks)"].max()
                durations.append(stage_time)  # Append summed stage time
            else:
                durations.append(stage_time)  # Append 0 if no steps exist

        # Add scenario duration column to the summary dataframe
        total_time_summary[f"{scenario.replace('_', ' ')} Duration (weeks)"] = durations

    # --- Compute time saved (positive = time saved) ---
    total_time_summary["Time Saved vs BAU (weeks)"] = (
            total_time_summary["BAU Duration (weeks)"] - total_time_summary["Proposed Tool Duration (weeks)"]
    )

    # --- Add Total row ---
    total_time_row = pd.DataFrame([{
        "Stage": "Total",
        "BAU Duration (weeks)": total_time_summary["BAU Duration (weeks)"].sum(),
        "Proposed Tool Duration (weeks)": total_time_summary["Proposed Tool Duration (weeks)"].sum(),
        "Time Saved vs BAU (weeks)": total_time_summary["Time Saved vs BAU (weeks)"].sum()
    }])

    # Append total row to the summary
    total_time_summary = pd.concat([total_time_summary, total_time_row], ignore_index=True)

    # ------------------------------------
    # --- Total Cost Per Project Stage ---
    # ------------------------------------
    cost_summary = pd.DataFrame({"Stage": project_stages})

    # --- Loop through each scenario (BAU and Proposed Tool) ---
    for scenario in ["BAU", "Proposed_Tool"]:
        costs = []

        # Retrieve the dataframe for the current scenario from session state
        df_scenario = st.session_state.get(f"df_{scenario}", pd.DataFrame())

        # Loop through each project stage
        for stage in project_stages:
            # Filter rows for the current stage; if empty, create an empty dataframe
            stage_rows = df_scenario[df_scenario["Stage"] == stage] if not df_scenario.empty else pd.DataFrame()

            stage_cost = 0  # Initialize stage cost accumulator

            # Loop through each row (role) in the stage
            for _, row in stage_rows.iterrows():
                role = row.get("Role", "")  # Role name
                pct_active = row.get("Active Time Spent (%)", 0)  # Percent time active
                duration_weeks = row.get("Total Duration (weeks)", 0)  # Duration in weeks

                # Look up the hourly rate for this role from personnel_rows
                hr_rate = next((p["Hourly Rate"] for p in personnel_rows if p["Role"] == role), 0)

                # Compute cost for this row: duration × active % × 40 hours/week × hourly rate
                stage_cost += duration_weeks * (pct_active / 100) * 40 * hr_rate

            # Append the total cost for this stage
            costs.append(stage_cost)

        # Add the scenario cost column to the summary dataframe
        cost_summary[f"{scenario.replace('_', ' ')} Cost ($)"] = costs

    # --- Add Infrastructure row ---
    infra_costs = st.session_state.get("df_infrastructure_costs", pd.DataFrame())
    if not infra_costs.empty:
        infra_row = {
            "Stage": "Infrastructure",
            "BAU Cost ($)": infra_costs.loc[infra_costs["Cost Category"] == "Total", "Business as Usual ($)"].values[0],
            "Proposed Tool Cost ($)":
                infra_costs.loc[infra_costs["Cost Category"] == "Total", "Proposed Tool ($)"].values[0]
        }
        cost_summary = pd.concat([cost_summary, pd.DataFrame([infra_row])], ignore_index=True)

    # --- Compute Cost Saved ---
    cost_summary["Cost Saved vs BAU ($)"] = cost_summary["BAU Cost ($)"] - cost_summary["Proposed Tool Cost ($)"]

    # --- Add Total row ---
    total_row = pd.DataFrame([{
        "Stage": "Total",
        "BAU Cost ($)": cost_summary["BAU Cost ($)"].sum(),
        "Proposed Tool Cost ($)": cost_summary["Proposed Tool Cost ($)"].sum(),
        "Cost Saved vs BAU ($)": cost_summary["Cost Saved vs BAU ($)"].sum()
    }])
    cost_summary = pd.concat([cost_summary, total_row], ignore_index=True)

    # --- Display tables ---
    st.markdown('### Duration (in weeks) by Project Stage ### ')
    st.info("""
            - This table presents the total duration per project stage (in weeks), ignoring personnel allocation and active time spent.
            - The **Total** row provides the overall project-level duration. 
            """)
    st.dataframe(total_time_summary, use_container_width=True)

    st.markdown('### Active Person-Hours by Project Stage ### ')
    st.info("""
            - This table presents the estimated total person-hours required for each stage of the research project across the **BAU** and **Proposed Tool** scenarios. 
            - **Time Saved** = hours saved by the Proposed Tool compared to BAU scenario (positive = less time required). 
            - All durations assume **40 working hours per week**. 
            - The **Total** row provides the overall project-level summary. 
            """)

    st.dataframe(time_summary, use_container_width=True)

    st.markdown('### Cost by Project Stage ### ')
    st.info("""
            - This table presents the estimated total personnel cost required for each stage of the research project as well as the non-personnel / infrastructure cost across the **BAU** and **Proposed Tool** scenarios. 
            - Personnel-cost is based on the % Active Time spent.
            - **Cost Saved** = hours saved by the Proposed Tool compared to BAU scenario (positive = less cost required). 
            - **Infrastructure** represents the total hardware / software cost (i.e. non personnel cost for the entire project)
            - The **Total** row provides the overall project-level summary. 
            """)
    st.dataframe(cost_summary, use_container_width=True)

elif page == "Personnel Efficiency Gains":
    st.header("📊 Personnel Efficiency Gains")

    # --- Retrieve DataFrames from session state ---
    df_bau = st.session_state.get("df_BAU_1", pd.DataFrame())  # Business as Usual scenario
    df_tool = st.session_state.get("df_Proposed_Tool", pd.DataFrame())  # Proposed Tool scenario
    personnel_rows = st.session_state.get("personnel_rows", [])  # List of personnel with hourly rates

    # --- Get unique roles across all scenarios ---
    roles = sorted({
        row.get("Role", "Unknown Role")
        for df in [df_bau, df_tool]
        for _, row in df.iterrows()
    })

    # --- Person-Hours Table ---
    time_summary = pd.DataFrame({"Role": roles})

    # Loop through scenarios and compute total hours per role
    for scenario_name, df_scenario in zip(["BAU", "Proposed Tool"], [df_bau, df_tool]):
        hours_list = []
        for role in roles:
            # Filter rows for current role
            role_rows = df_scenario[df_scenario["Role"] == role] if not df_scenario.empty else pd.DataFrame()
            # Sum total active hours: duration_weeks * % active * 40 hours/week
            total_hours = sum(
                row.get("Total Duration (weeks)", 0) * row.get("Active Time Spent (%)", 0) / 100 * 40
                for _, row in role_rows.iterrows()
            )
            hours_list.append(total_hours)
        time_summary[f"{scenario_name} (hrs)"] = hours_list

    # Compute time saved (positive = hours saved)
    time_summary["Time Saved vs BAU (hrs)"] = (
            time_summary["BAU (hrs)"] - time_summary["Proposed Tool (hrs)"]
    )

    # Add Total row
    total_time_row = pd.DataFrame([{
        "Role": "Total",
        "BAU (hrs)": time_summary["BAU (hrs)"].sum(),
        "Proposed Tool (hrs)": time_summary["Proposed Tool (hrs)"].sum(),
        "Time Saved vs BAU (hrs)": time_summary["Time Saved vs BAU (hrs)"].sum()
    }])
    time_summary = pd.concat([time_summary, total_time_row], ignore_index=True)

    # --- Cost Table ---
    cost_summary = pd.DataFrame({"Role": roles})

    # Loop through scenarios and compute total cost per role
    for scenario_name, df_scenario in zip(["BAU", "Proposed Tool"], [df_bau, df_tool]):
        cost_list = []
        for role in roles:
            role_rows = df_scenario[df_scenario["Role"] == role] if not df_scenario.empty else pd.DataFrame()
            total_cost = 0
            for _, row in role_rows.iterrows():
                pct_active = row.get("Active Time Spent (%)", 0)
                duration_weeks = row.get("Total Duration (weeks)", 0)
                # Look up hourly rate for this role
                hr_rate = next((p["Hourly Rate"] for p in personnel_rows if p["Role"] == role), 0)
                # Compute cost for this row and accumulate
                total_cost += duration_weeks * pct_active / 100 * 40 * hr_rate
            cost_list.append(total_cost)
        cost_summary[f"{scenario_name} Cost ($)"] = cost_list

    # Compute cost saved (positive = cost saved)
    cost_summary["Cost Saved vs BAU ($)"] = (
            cost_summary["BAU Cost ($)"] - cost_summary["Proposed Tool Cost ($)"]
    )

    # Add Total row for costs
    total_cost_row = pd.DataFrame([{
        "Role": "Total",
        "BAU Cost ($)": cost_summary["BAU Cost ($)"].sum(),
        "Proposed Tool Cost ($)": cost_summary["Proposed Tool Cost ($)"].sum(),
        "Cost Saved vs BAU ($)": cost_summary["Cost Saved vs BAU ($)"].sum()
    }])
    cost_summary = pd.concat([cost_summary, total_cost_row], ignore_index=True)

    # --- Display Person-Hours Table ---
    st.markdown('### Active Person-Hours by Role ### ')
    st.info("""
        - Shows total active hours per role across **BAU** and **Proposed Tool** scenarios.
        - **Time Saved** = hours saved by Proposed Tool compared to BAU (positive = less time required).
        - All durations assume 40 working hours per week.
        - The **Total** row provides the overall summary across all roles.
    """)
    st.dataframe(time_summary, use_container_width=True)

    # --- Display Cost Table ---
    st.markdown('### Personnel Cost by Role ### ')
    st.info("""
        - Shows total personnel cost per role across **BAU** and **Proposed Tool** scenarios.
        - Personnel cost is based on the % Active Time spent.
        - Cost Saved = hours saved by the Proposed Tool compared to BAU (positive = less cost required).
        - The Total row provides the overall project-level summary.
    """)
    st.dataframe(cost_summary, use_container_width=True)

elif page == "Social ROI":
    st.header("📈 Social Return on Investment (ROI) Analysis")

    # --- Section: Impact per Study ---
    st.markdown("#### Impact per Study")
    st.info(
        "Impact per Study is defined from the Social ROI Parameters as:\n\n"
        "***Discovery Rate*** × ***Per-student improvement in long-term economic opportunity*** × ***Total Reach*** "
        "(i.e., number of students impacted by the research study)"
    )

    # --- Retrieve total project durations in weeks ---
    durations_weeks = {}
    for scenario in ["BAU", "Proposed_Tool"]:
        df_scenario = st.session_state.get(f"df_{scenario}", pd.DataFrame())
        total_weeks = 0
        if not df_scenario.empty:
            # Sum the maximum duration per stage
            total_weeks = df_scenario.groupby("Stage")["Total Duration (weeks)"].max().sum()
        durations_weeks[scenario] = total_weeks

    # Convert weeks to months (approx 4.345 weeks/month)
    durations_months = {k: v / 4.345 for k, v in durations_weeks.items()}

    # --- Retrieve total costs (personnel + infrastructure) ---
    cost_summary = st.session_state.get("df_infrastructure_costs", pd.DataFrame())
    total_costs = {}
    for scenario in ["BAU", "Proposed_Tool"]:
        # Infrastructure cost
        infra_cost = 0
        if not cost_summary.empty:
            if scenario == "BAU":
                infra_cost = cost_summary.loc[cost_summary["Cost Category"] == "Total", "Business as Usual ($)"].values[
                    0]
            else:
                infra_cost = cost_summary.loc[cost_summary["Cost Category"] == "Total", "Proposed Tool ($)"].values[0]

        # Personnel cost
        df_scenario = st.session_state.get(f"df_{scenario}", pd.DataFrame())
        personnel_rows = st.session_state.get("personnel_rows", [])
        personnel_cost = 0
        for _, row in df_scenario.iterrows():
            role = row.get("Role", "")
            pct_active = row.get("Active Time Spent (%)", 0)
            duration_weeks = row.get("Total Duration (weeks)", 0)
            hr_rate = next((p["Hourly Rate"] for p in personnel_rows if p["Role"] == role), 0)
            personnel_cost += duration_weeks * pct_active / 100 * 40 * hr_rate

        total_costs[scenario] = infra_cost + personnel_cost

    # --- Compute Impact per Study ---
    roi_params = st.session_state.get("roi_parameters", {})
    per_student_improvement = roi_params.get("computed_improvement", 0)
    discovery_rate = roi_params.get("discovery_rate", 0) / 100
    total_students = roi_params.get("total_students", 0)

    impact_per_study = {
        scenario: per_student_improvement * discovery_rate * total_students
        for scenario in ["BAU", "Proposed_Tool"]
    }

    # --- Build ROI DataFrame ---
    roi_df = pd.DataFrame({
        "Scenario": ["BAU", "Proposed Tool"],
        "Time (months)": [round(durations_months["BAU"], 1), round(durations_months["Proposed_Tool"], 1)],
        "Cost ($)": [round(total_costs["BAU"], 2), round(total_costs["Proposed_Tool"], 2)],
        "Impact per study ($)": [round(impact_per_study["BAU"], 2), round(impact_per_study["Proposed_Tool"], 2)]
    })
    st.dataframe(roi_df, use_container_width=True)

    # --- Retrieve additional ROI parameters ---
    num_orgs_bau = roi_params.get("orgs_bau", 0)
    num_orgs_proposed = roi_params.get("orgs_proposed", 0)
    total_investment = roi_params.get("total_investment", 0)
    num_concurrent_projects = roi_params.get("concurrent_studies", 0)

    bau_time = get_scenario_value("BAU", "Time (months)")
    tool_time = get_scenario_value("Proposed Tool", "Time (months)")
    bau_cost = get_scenario_value("BAU", "Cost ($)")
    tool_cost = get_scenario_value("Proposed Tool", "Cost ($)")
    bau_impact = get_scenario_value("BAU", "Impact per study ($)")
    tool_impact = get_scenario_value("Proposed Tool", "Impact per study ($)")

    # === User Inputs for Fixed Costs ===
    st.markdown('---')
    st.markdown("#### ⚙️ Adjust Fixed Costs (optional)")

    st.info(
        """
        - **Fixed Costs**
            - One-time or upfront expenses that do not vary with the number of research studies conducted, typically covering the setup and development of the solution.
            - Examples include tool development, software setup, infrastructure installation, 
        and initial onboarding or training. 
            - This cost is **separate** from the operational cost of a research 
        study. 
        
        - **Variable Costs** 
            - These are recurring or scalable expenses that are incurred for each research study. 
            - Examples include data storage, API or tool usage, researcher time, or other per-study fees. 
            - This cost is **derived directly** from the operational cost of the research study. 
        
        **Note: The operational cost of the research study is the total personnel and infrastructure costs computed 
        from your inputs**. """)

    col1, col2 = st.columns(2)
    with col1:
        fixed_bau_user = st.number_input(
            "BAU Fixed Cost ($)",
            value=0,
            help="""One-time setup cost for the BAU scenario."""
        )
        st.caption("""This is initialized to $0, assuming that without the proposed tool, organizations repeat 
        the setup for each new project (i.e., there are no one-time costs; all costs are per project). 
        Depending on the typical BAU scenario for the organizations targeted by the proposed tool—such as whether 
        they would build a custom tool, use an off-the-shelf solution, or repeat the setup for each project—please provide 
        your best estimate of their initial setup cost. """)

    with col2:
        fixed_tool_user = st.number_input(
            "Proposed Tool Fixed Cost ($)",
            value=total_investment,
            help="""Initial investment or one-time setup cost in the Proposed Tool scenario"""
        )
        st.caption("""This is initialized to the grantee organization's investment in building the proposed tool.
        Adjusted as needed to reflect actual or projected costs.""")

    # === Charts: Impact per Dollar Over Time ===
    st.markdown('---')
    st.markdown("### 📉 Impact per Dollar Over Time")

    # Compute projections for each scenario
    projection_data_bau = compute_projection("BAU", bau_time, bau_cost, bau_impact,
                                             fixed_bau_user, num_orgs_bau, num_concurrent_projects)
    projection_data_pt = compute_projection("Proposed Tool", tool_time, tool_cost, tool_impact,
                                            fixed_tool_user, num_orgs_proposed, num_concurrent_projects)

    # Convert projections to DataFrames
    roi_projection_bau = pd.DataFrame(projection_data_bau)
    roi_projection_pt = pd.DataFrame(projection_data_pt)
    roi_projection_all = pd.concat([roi_projection_bau, roi_projection_pt])

    # --- Plot 1: Variable Cost Only ---
    fig1 = px.line(
        roi_projection_all,
        x="Year",
        y="Impact per $ (Variable only)",
        color="Scenario",
        title="Impact per $ (Variable Cost)",
        markers=True
    )
    st.plotly_chart(fig1, use_container_width=True)

    # --- Plot 2: Total Cost (Fixed + Variable) ---
    fig2 = px.line(
        roi_projection_all,
        x="Year",
        y="Impact per $ (Total cost)",
        color="Scenario",
        title="Impact per Dollar (Including Fixed + Variable Costs)",
        markers=True
    )
    st.plotly_chart(fig2, use_container_width=True)

    # --- Display Data Table ---
    st.markdown("##### Social ROI Data Table")
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
            if st.button("⬅️Back", key="back"):
                go_back()
                st.rerun()

    with col3:
        if current_idx < len(PAGES) - 1:
            if st.button("Next ➡️", key="next"):
                go_next()
                st.rerun()
        elif current_idx == len(PAGES) - 1:
            if st.button("🔁Reset", key="restart"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                go_first()
                st.rerun()  # Reloads the app from the top
