import streamlit as st
import pandas as pd
import uuid

# --- Page configuration ---
st.set_page_config(
    page_title="ROI and Cost Analysis Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"  # Keep sidebar open
)

# --- Define pages and hierarchy ---
PAGE_GROUPS = {
    "Instructions How-to-use": [],
    "Inputs": {
        "Personnel Salaries": [],
        "Infrastructure Costs": [],
        "ROI Parameters": [],
        "Assumptions": [],
        "Project Activities": ["BAU 1", "BAU 2", "Proposed Tool"],
    },
    "Outputs Tables and Graphs": []
}

# Flatten pages for sequential navigation
PAGES = [
    "Instructions How-to-use",
    "Personnel Salaries",
    "Infrastructure Costs",
    "ROI Parameters",
    "Assumptions",
    "BAU 1",
    "BAU 2",
    "Proposed Tool",
    "Outputs Tables and Graphs"
]

# --- Initialize session state ---
if "current_page" not in st.session_state:
    st.session_state.current_page = "Instructions How-to-use"

# --- Sidebar Navigation ---
st.sidebar.title("Sidebar Navigation")

st.sidebar.markdown("### 🧭 Navigation")
if st.sidebar.button("📘 Instructions (How-to-use)", use_container_width=True):
    st.session_state.current_page = "Instructions How-to-use"

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
if st.sidebar.button("📈 Outputs (Tables and Graphs)", use_container_width=True):
    st.session_state.current_page = "Outputs Tables and Graphs"

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
        "BAU 1": {},
        "BAU 2": {},
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
    "Data Sharing Agreements & Data User Agreements",
    "Human Subject Research Approvals",
    "Data Collection & Access or Transfer",
    "Data Cleaning",
    "Study Design & Infrastructure Setup",
    "Study Implementation and Monitoring",
    "Data Modeling & Analysis",
    "Reporting"
]

# --- Helper function to render activity sections ---
def render_activity_section(section_name):
    st.caption(
        "You may edit, replace, or enter N/A for the activities so that they align with the type of projects your tool supports. "
        "The listed activities are only intended as examples. Where relevant, please include a brief description (1-2 lines) "
        "of the activity. Overall project stage titles remain unchanged as a consistent framework across projects."
    )

    # List to collect all preview data
    all_preview_data = []

    for stage in project_stages:
        with st.expander(stage, expanded=False):
            # Initialize storage with prefilled steps if empty
            if stage not in st.session_state.project_steps[section_name]:
                st.session_state.project_steps[section_name][stage] = []

                # Stage-specific prefilled steps
                if stage == 'Data Sharing Agreements & Data User Agreements':
                    st.session_state.project_steps[section_name][stage] = [{
                        "id": str(uuid.uuid4()),
                        "Step": "Drafting agreements, review, executing DSAs and DUAs",
                        "Notes": "",
                        "Duration": 0.0,
                        "Roles": {r: 0.0 for r in personnel_roles}
                    }]
                elif stage == 'Human Subject Research Approvals':
                    st.session_state.project_steps[section_name][stage] = [
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
                            "Notes": "",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                elif stage == 'Data Collection & Access or Transfer':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Data Collection, Documentation, Anonymization (i.e. Data setup)",
                            "Notes": "",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        },
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Secure data access / transfer to researchers",
                            "Notes": "",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                elif stage == 'Data Cleaning':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Data Review or Quality Check, Data Cleaning & Merging",
                            "Notes": "",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                elif stage == 'Study Design & Infrastructure Setup':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Exploratory Data Analysis to guide Study Design",
                            "Notes": "",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        },
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Data preparation to implement the study",
                            "Notes": "",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        },
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Setting up the infrastructure to execute or run the experiment",
                            "Notes": "",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                elif stage == 'Study Implementation and Monitoring':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Run the study",
                            "Notes": "",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                elif stage == 'Data Modeling & Analysis':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Analysis & QA",
                            "Notes": "",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                elif stage == 'Reporting':
                    st.session_state.project_steps[section_name][stage] = [
                        {
                            "id": str(uuid.uuid4()),
                            "Step": "Report writing & communications",
                            "Notes": "",
                            "Duration": 0.0,
                            "Roles": {r: 0.0 for r in personnel_roles}
                        }
                    ]
                else:
                    st.session_state.project_steps[section_name][stage] = [{
                        "id": str(uuid.uuid4()),
                        "Step": "<placeholder>",
                        "Notes": "",
                        "Duration": 0.0,
                        "Roles": {r: 0.0 for r in personnel_roles}
                    }]

            rows = st.session_state.project_steps[section_name][stage]

            for idx, row in enumerate(rows.copy()):
                st.markdown(f"""
                <div style="
                    background-color: #c2e5d3; 
                    padding: 15px; 
                    border-radius: 8px; 
                    margin-bottom: 15px;
                    border: 1px solid #c2e5d3;
                ">
                """, unsafe_allow_html=True)

                st.markdown(f"**Step {idx+1}**")

                # Step Description + Notes
                cols1 = st.columns([4, 4])
                step_desc = cols1[0].text_area(
                    "Step Description",
                    value=row.get("Step", "<placeholder>"),
                    key=f"{section_name}_{stage}_step_{row['id']}",
                    height=80
                )
                notes = cols1[1].text_area(
                    "Notes (Explain how time/labor is affected by BAU 1/ BAU 2/Proposed Tool)",
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

                # Active Time per Role
                st.markdown("**% Active Time per Role**")
                time_data = {}
                for role in personnel_roles:
                    val = st.number_input(
                        f"{role}",
                        min_value=0.0,
                        step=1.0,
                        value=row.get("Roles", {}).get(role, 0.0),
                        format="%.2f",
                        key=f"{section_name}_{stage}_{role}_{row['id']}"
                    )
                    time_data[role] = val
                row["Roles"] = time_data

                # Delete Step
                if st.button("❌ Delete Step", key=f"del_{section_name}_{stage}_{row['id']}"):
                    st.session_state.project_steps[section_name][stage] = [
                        r for r in rows if r["id"] != row["id"]
                    ]
                    st.rerun()

                st.markdown("</div>", unsafe_allow_html=True)

            # Add new step
            if st.button(f"➕ Add Step to {stage}", key=f"add_{section_name}_{stage}"):
                new_row = {
                    "id": str(uuid.uuid4()),
                    "Step": "<placeholder>",
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
if page == "Instructions How-to-use":
    st.markdown("---")
    st.markdown("## 🧭 Instructions (How-to-use)")
    st.markdown("---")

    st.subheader("▶️ Tutorial Video")
    st.video("https://www.youtube.com/watch?v=_4kHxtiuML0")  # replace with your link

    st.subheader("📘 Step-by-Step Instructions")
    st.markdown("""
    1. **Use the Sidebar** to navigate between pages.  
    2. **Enter Input Data** (Salaries, Activities, Costs, etc.).  
    3. **Adjust ROI Parameters** and **set Assumptions**.  
    4. **View Outputs** with results and visualizations.  
    5. Use **Next** and **Back** buttons for linear navigation.
    """)

# =========================================================
#  PERSONNEL SALARIES PAGE
# =========================================================
elif page == "Personnel Salaries":
    st.markdown("---")
    st.header("💼 Personnel Salaries")
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

        st.markdown(f"**Role #{idx+1}**")
        cols = st.columns([3, 2, 4, 1])  # Narrow column for trash icon

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
    st.write("### Current Personnel Table")
    personnel_salaries_df = pd.DataFrame(st.session_state.personnel_rows).drop(columns="id")
    st.dataframe(personnel_salaries_df, use_container_width=True)
    st.session_state[f"df_personnel_salaries"] = personnel_salaries_df

    # CSV Download
    if len(st.session_state.personnel_rows) > 0:
        df_download = pd.DataFrame(st.session_state.personnel_rows).drop(columns="id")
        csv = df_download.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Table as CSV",
            data=csv,
            file_name="personnel_table.csv",
            mime="text/csv"
        )

# =========================================================
#  PROJECT ACTIVITIES PAGE
# =========================================================
elif page == "BAU 1":
    st.markdown("---")
    st.header("📊 BAU 1: Project Activities")
    st.markdown("---")

    render_activity_section("BAU 1")

elif page == "BAU 2":
    st.markdown("---")
    st.header("📊 BAU 2: Project Activities")
    st.markdown("---")

    if st.button("📋 Copy all values from BAU 1"):
        copy_from_section("BAU 1", "BAU 2")

    render_activity_section("BAU 2")

elif page == "Proposed Tool":
    st.markdown("---")
    st.header("📊 Proposed Tool: Project Activities")
    st.markdown("---")

    if st.button("📋 Copy all values from BAU 1"):
        copy_from_section("BAU 1", "Proposed Tool")

    if st.button("📋 Copy all values from BAU 2"):
        copy_from_section("BAU 2", "Proposed Tool")

    render_activity_section("Proposed Tool")

# =========================================================
#  ROI PARAMETERS PAGE
# =========================================================
elif page == "ROI Parameters":
    st.markdown("---")
    st.header("📈 ROI Parameters")
    st.markdown("---")

    # --- Median Impact on Learning Outcomes ---
    st.subheader("Estimated Impact of Research Project")
    col1, col2 = st.columns([3, 1])
    with col1:
        learning_definition = st.text_input(
            "Definition of median impact on learning outcomes (in SD terms)",
            placeholder="e.g., Median impact on standardized math scores (in SD)"
        )
    with col2:
        learning_sd = st.number_input(
            "Median impact (SD)",
            min_value=0.0,
            placeholder=0.12,
            step=0.01,
            format="%.2f",
            key="roi_learning_sd"
        )

    # --- Economic Opportunity Coefficient ---
    econ_definition = st.text_input(
        "Definition of average increase in long-term economic opportunity per 1 SD improvement (in $ terms)",
        placeholder="e.g. avg. increase in income at 30 for 1 SD improvement in math scores in middle school"
    )
    econ_per_sd = st.number_input(
        "Average Economic increase per 1 SD (in $)",
        min_value=0.0,
        placeholder=2400,
        step=0.01,
        format="%.2f",
        key="roi_econ_per_sd"
    )

    # --- Per-Student Outcome Improvement (Computed) ---
    computed_improvement = learning_sd * econ_per_sd
    st.number_input("Per-student improvement in long-term economic opportunity (in $)", value=computed_improvement,
                    disabled=True)

    # --- Evidence Generation ---
    st.subheader("Evidence / Discovery Rate")
    evidence_rate = st.number_input(
        "Rate of discovery of impact",
        min_value=0.0,
        step=0.01,
        format="%.2f",
        key="roi_evidence_rate"
    )

    # --- Reach & Investment ---
    st.subheader("Reach & Investment")
    total_students = st.number_input(
        "Total number of students served by platform / tool",
        min_value=1,
        step=1,
        key="roi_total_students"
    )
    total_investment = st.number_input(
        "Total investment by grant organization in the tool (in $)",
        min_value=0,
        step=1000,
        format="%d",
        key="roi_total_investment_k"
    )

    # --- Organizations Served ---
    st.subheader("Organizations Served")
    orgs_proposed = st.number_input(
        "Number of organizations served by proposed tool",
        min_value=1,
        step=1,
        key="roi_orgs_proposed"
    )
    orgs_bau1 = st.number_input(
        "Number of organizations served under BAU scenario 1",
        min_value=1,
        step=1,
        key="roi_orgs_bau1"
    )
    orgs_bau2 = st.number_input(
        "Number of organizations served under BAU scenario 2",
        min_value=1,
        step=1,
        key="roi_orgs_bau2"
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
        "total_investment_k": total_investment,
        "orgs_proposed": orgs_proposed,
        "orgs_bau1": orgs_bau1,
        "orgs_bau2": orgs_bau2
    }

    st.markdown("✅ ROI parameters (including computed improvement) saved.")

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
    csv = df_assumptions.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Assumptions as CSV",
        data=csv,
        file_name="assumptions.csv",
        mime="text/csv"
    )
# =========================================================
#  INFRASTRUCTURE PAGE
# =========================================================
elif page == "Infrastructure Costs":
    st.markdown("---")
    st.header("🏗️ Infrastructure Costs")
    st.markdown("---")

    st.caption(
        "Enter annual infrastructure or operational costs for each scenario below. "
        "You can adjust cost amounts, add notes, and compute per-study costs automatically."
    )

    # --- Notes ---
    st.info(
        "The cost estimate reflects the **total cost incurred per study**, i.e., for the end-users who are:\n"
        "- researchers and organizations that integrate the proposed tool or build their own (as in BAUs), and\n"
        "- the platform that maintains the proposed tool."
    )

    # --- Initialize with prefilled categories but no costs ---
    if "infrastructure_costs" not in st.session_state:
        st.session_state.infrastructure_costs = [
            {
                "id": str(uuid.uuid4()),
                "Cost Category (annual costs)": "Integration Costs",
                "BAU 1": 0.0,
                "BAU 2": 0.0,
                "Proposed Tool": 0.0,
                "Notes / Assumptions": ""
            },
            {
                "id": str(uuid.uuid4()),
                "Cost Category (annual costs)": "Software Licenses",
                "BAU 1": 0.0,
                "BAU 2": 0.0,
                "Proposed Tool": 0.0,
                "Notes / Assumptions": ""
            },
            {
                "id": str(uuid.uuid4()),
                "Cost Category (annual costs)": "Compute Resources",
                "BAU 1": 0.0,
                "BAU 2": 0.0,
                "Proposed Tool": 0.0,
                "Notes / Assumptions": ""
            },
            {
                "id": str(uuid.uuid4()),
                "Cost Category (annual costs)": "Storage",
                "BAU 1": 0.0,
                "BAU 2": 0.0,
                "Proposed Tool": 0.0,
                "Notes / Assumptions": ""
            }
        ]

    # --- Editable Cost Inputs ---
    rows = st.session_state.infrastructure_costs
    for idx, row in enumerate(rows):
        st.markdown(f"Cost Item #{idx + 1}")
        cols = st.columns([3, 1, 1, 1, 3, 1])

        category = cols[0].text_input(
            "Cost Category (annual costs)",
            value=row["Cost Category (annual costs)"],
            key=f"cat_{row['id']}"
        )
        bau1 = cols[1].number_input(
            "BAU 1",
            min_value=0.0,
            step=10.0,
            value=float(row["BAU 1"]),
            key=f"bau1_{row['id']}"
        )
        bau2 = cols[2].number_input(
            "BAU 2",
            min_value=0.0,
            step=10.0,
            value=float(row["BAU 2"]),
            key=f"bau2_{row['id']}"
        )
        proposed = cols[3].number_input(
            "Prop. Tool",
            min_value=0.0,
            step=10.0,
            value=float(row["Proposed Tool"]),
            key=f"tool_{row['id']}"
        )
        notes = cols[4].text_input(
            "Notes / Assumptions",
            value=row["Notes / Assumptions"],
            key=f"notes_{row['id']}"
        )

        if cols[5].button("❌", key=f"del_cost_{row['id']}"):
            st.session_state.infrastructure_costs = [r for r in rows if r["id"] != row["id"]]
            st.rerun()

        # Update stored row
        row.update({
            "Cost Category (annual costs)": category,
            "BAU 1": bau1,
            "BAU 2": bau2,
            "Proposed Tool": proposed,
            "Notes / Assumptions": notes
        })

    # --- Add new row button ---
    if st.button("➕ Add Additional Cost Category"):
        st.session_state.infrastructure_costs.append({
            "id": str(uuid.uuid4()),
            "Cost Category (annual costs)": "",
            "BAU 1": 0.0,
            "BAU 2": 0.0,
            "Proposed Tool": 0.0,
            "Notes / Assumptions": ""
        })
        st.rerun()

    # --- Convert to DataFrame ---
    df_infra = pd.DataFrame(st.session_state.infrastructure_costs).drop(columns="id")


    # --- Studies conducted per year ---
    studies_per_year = st.number_input(
        "📚 Studies Conducted per Year",
        min_value=1.0,
        step=1.0,
        value=10.0,
        format="%.0f"
    )

    # --- Compute totals ---
    total_bau1 = df_infra["BAU 1"].sum()
    total_bau2 = df_infra["BAU 2"].sum()
    total_tool = df_infra["Proposed Tool"].sum()

    per_study_bau1 = total_bau1 / studies_per_year
    per_study_bau2 = total_bau2 / studies_per_year
    per_study_tool = total_tool / studies_per_year

    # --- Itemized Preview Table ---
    st.markdown("### 🧾 Itemized Infrastructure Costs")
    st.dataframe(df_infra, use_container_width=True)

    # --- Summary Preview Table ---
    st.markdown("### 💰 Summary of Total & Per-Study Costs")
    summary_df = pd.DataFrame({
        "Scenario": ["BAU 1", "BAU 2", "Proposed Tool"],
        "Total Annual Cost ($ thousands)": [total_bau1, total_bau2, total_tool],
        "Per-Study Cost ($ thousands per study)": [per_study_bau1, per_study_bau2, per_study_tool]
    })
    st.dataframe(summary_df, use_container_width=True)

    # --- CSV download for itemized table ---
    csv_infra = df_infra.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Itemized Infrastructure Costs as CSV",
        data=csv_infra,
        file_name="infrastructure_costs_itemized.csv",
        mime="text/csv"
    )

    # --- Store DataFrames for later use ---
    st.session_state.df_infrastructure_costs = df_infra
    st.session_state.df_infrastructure_summary = summary_df


# =========================================================
#  OUTPUT PAGE
# =========================================================
elif page == "Outputs Tables and Graphs":
    st.header("Outputs (Tables and Graphs)")
    st.success("✅ You’ve reached the final section!")
    st.write("Results, charts, and performance indicators will appear here.")

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
            if st.button("🔁 Restart (Go to First Page)", key="restart"):
                go_first()
                st.rerun()