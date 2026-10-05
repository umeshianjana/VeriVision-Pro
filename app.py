import streamlit as st
import re
import graphviz

st.set_page_config(page_title="VeriVision Pro - AI RTL Visualizer & Verification Suite", page_icon="⚡", layout="wide")

# Title Header
st.title("⚡ VeriVision Pro: RTL Logic Visualizer & Static Linter")
st.caption("EDA Playground-style Hardware Verification Suite & AI Assistant for Digital Engineers.")

# Sidebar Controls
st.sidebar.header("⚙️ Control Panel")
theme_choice = st.sidebar.selectbox("Schematic Theme", ["Default Light", "High Contrast", "Blueprint"])

# Quick Verilog Templates
st.sidebar.markdown("---")
st.sidebar.subheader("📚 Quick Verilog Templates")
template = st.sidebar.radio("Select Template", ["2-to-1 MUX & FlipFlop", "Simple AND Gate", "Full Adder"])

# Business Pricing Tiers
st.sidebar.markdown("---")
st.sidebar.subheader("💎 Subscription Tier")
user_plan = st.sidebar.radio(
    "Active Plan",
    ["🎓 Free (Open Source)", "⚡ Pro Designer ($19/mo)", "🏢 Enterprise ($149/mo)"]
)

if user_plan == "🎓 Free (Open Source)":
    st.sidebar.info("Free Plan Active: Basic RTL Schematic enabled. Upgrade to Pro for AI Linter.")
elif user_plan == "⚡ Pro Designer ($19/mo)":
    st.sidebar.success("Pro Active: AI Auto-Fix suggestions & static linter fully unlocked!")
else:
    st.sidebar.success("Enterprise Active: Full Suite, CI/CD linting & priority AI support unlocked!")

# Default Templates
sample_code = """module mux2to1 (
    input wire a,
    input wire b,
    input wire sel,
    input wire clk,
    output reg y,
    output wire unused_wire
);

wire sel_n;
wire out_a;
wire out_b;

assign sel_n = ~sel;
assign out_a = a & sel_n;
assign out_b = b & sel;

always @(posedge clk) begin
    if (sel)
        y <= b;
    else
        y <= a;
end
endmodule"""

if template == "Simple AND Gate":
    sample_code = """module and_gate (
    input wire in1,
    input wire in2,
    output wire out
);
assign out = in1 & in2;
endmodule"""
elif template == "Full Adder":
    sample_code = """module full_adder (
    input wire a, b, cin,
    output wire sum, cout
);
assign sum = a ^ b ^ cin;
assign cout = (a & b) | (cin & (a ^ b));
endmodule"""

# Code Editor
verilog_code = st.text_area(
    "📝 Paste / Edit Verilog Code Here (Press Ctrl+Enter to apply changes):",
    value=sample_code,
    height=240,
    key="verilog_editor"
)

# Action Buttons
c_btn1, c_btn2 = st.columns([1, 3])
with c_btn1:
    if st.button("🚀 Run & Analyze", type="primary"):
        st.rerun()
with c_btn2:
    st.download_button(
        label="📥 Download Verilog File (.v)",
        data=verilog_code,
        file_name="design.v",
        mime="text/x-verilog"
    )

st.markdown("---")

# EDA PLAYGROUND SYNTAX VALIDATOR
def validate_syntax(code):
    syntax_errors = []
    # 1. Check Module Declaration & Closing
    if "module" not in code:
        syntax_errors.append("Syntax Error: Missing module keyword declaration.")
    if "endmodule" not in code:
        syntax_errors.append("Syntax Error: Missing endmodule keyword at the end of design.")
        
    # 2. Check Illegal Characters / Typos outside comments
    clean_lines = [line.split("//")[0].strip() for line in code.split("\n")]
    full_clean = " ".join(clean_lines)
    
    # Unmatched parentheses check
    if full_clean.count("(") != full_clean.count(")"):
        syntax_errors.append("Syntax Error: Unmatched parentheses () detected in port list or expression.")
        
    # Invalid keywords
    invalid_keywords = re.findall(r'\b(wgire|inpu|outpu|assig|alway)\b', full_clean)
    if invalid_keywords:
        for ik in set(invalid_keywords):
            syntax_errors.append(f"Syntax Error: Invalid or misspelled Verilog keyword '{ik}' detected.")
            
    return syntax_errors

# ROBUST PARSER ENGINE
def parse_verilog(code):
    clean_code = re.sub(r'//.*', '', code)
    
    modules = re.findall(r'module\s+([a-zA-Z_]\w*)', clean_code)
    module_name = modules[0] if modules else "UnknownModule"
    
    inputs = list(dict.fromkeys(re.findall(r'\binput\s+(?:wire|reg)?\s*\[?\d*:?\d*\]?\s*([a-zA-Z_]\w*)', clean_code)))
    outputs = list(dict.fromkeys(re.findall(r'\boutput\s+(?:wire|reg)?\s*\[?\d*:?\d*\]?\s*([a-zA-Z_]\w*)', clean_code)))
    wires = list(dict.fromkeys(re.findall(r'\bwire\s+\[?\d*:?\d*\]?\s*([a-zA-Z_]\w*)', clean_code)))
    regs = list(dict.fromkeys(re.findall(r'\breg\s+\[?\d*:?\d*\]?\s*([a-zA-Z_]\w*)', clean_code)))
    
    wires = [w for w in wires if w not in inputs and w not in outputs]
    regs = [r for r in regs if r not in inputs and r not in outputs]
    
    assigns = re.findall(r'assign\s+([a-zA-Z_]\w*)\s*=\s*([^;]+);', clean_code)
    
    return module_name, inputs, outputs, wires, regs, assigns

# Run Validation
syntax_bugs = validate_syntax(verilog_code)

if syntax_bugs:
    st.error("🚨 EDA Syntax Compilation Failed! Please fix the syntax errors below before generating schematic:")
    for err in syntax_bugs:
        st.error(f"❌ {err}")
else:
    mod_name, inputs, outputs, wires, regs, assigns = parse_verilog(verilog_code)
    
    # TABBED VIEW ARCHITECTURE
    tab1, tab2, tab3 = st.tabs(["🛠️ RTL Schematic & Logic Flow", "🔍 Linter & AI Code Fixer", "📊 Hardware AST Summary"])
    
    # TAB 1: SCHEMATIC
    with tab1:
        if verilog_code.strip():
            dot = graphviz.Digraph(comment='Verilog RTL Flow')
            dot.attr(rankdir='LR', size='10,6')
            
            node_fill = "lightblue" if theme_choice == "Default Light" else "yellow" if theme_choice == "High Contrast" else "cyan"
            
            if inputs:
                with dot.subgraph(name='cluster_inputs') as c:
                    c.attr(label='Inputs', color='blue')
                    for inp in inputs:
                        c.node(inp, shape='cds', style='filled', fillcolor=node_fill)
                        
            if outputs:
                with dot.subgraph(name='cluster_outputs') as c:
                    c.attr(label='Outputs', color='green')
                    for out in outputs:
                        c.node(out, shape='cds', style='filled', fillcolor='lightgreen')
                        
            for dest, expr in assigns:
                gate_node = f"Gate_{dest}"
                dot.node(gate_node, label=f"Assign Logic\n{dest} = {expr.strip()}", shape='box', style='rounded,filled', fillcolor='whitesmoke')
                
                for var in set(inputs + wires + regs):
                    if re.search(rf'\b{var}\b', expr) and var != dest:
                        dot.edge(var, gate_node)
                        
                if dest in outputs or dest in wires or dest in regs:
                    dot.edge(gate_node, dest)
                    
            st.graphviz_chart(dot, use_container_width=True)
            
    # TAB 2: LINTER & AI FIXER
    with tab2:
        if user_plan == "🎓 Free (Open Source)":
            st.warning("⚠️ **Linter & AI Code Fixer is a Pro / Enterprise Feature**")
            st.info("Please select **⚡ Pro Designer ($19/mo)** or **🏢 Enterprise ($149/mo)** in the sidebar to unlock automated static linting!")
        else:
            st.subheader(f"🔍 Static Analysis for Module: {mod_name}")
            warnings = []
            
            clean_code = re.sub(r'//.*', '', verilog_code)
            all_declared = set(inputs + outputs + wires + regs)
            
            for var in all_declared:
                if len(re.findall(rf'\b{var}\b', clean_code)) <= 1:
                    warnings.append(f"Unused Signal: {var} is declared but never driven or referenced.")
                    
            if "always" in verilog_code and "=" in verilog_code and "<=" not in verilog_code:
                warnings.append("Coding Style Violation: Sequential always block detected with blocking assignment (=) instead of (<=).")
                
            if warnings:
                for w in warnings:
                    st.warning(f"⚠️ {w}")
                st.markdown("---")
                st.subheader("💡 AI Auto-Fix Assistant Suggestion")
                st.info("The AI engine suggests removing unused signals and switching to non-blocking assignments:")
                
                cleaned_code = verilog_code
                for var in all_declared:
                    if len(re.findall(rf'\b{var}\b', clean_code)) <= 1:
                        cleaned_code = re.sub(rf'.*{var}.*\n?', '', cleaned_code)
                        
                st.code(cleaned_code, language="verilog")
            else:
                st.success("✅ Clean Code! Zero static linting warnings detected in the design.")
                
    # TAB 3: HARDWARE AST METRICS
    with tab3:
        st.subheader("📊 Hardware Module Specs")
        sc1, sc2, sc3, sc4 = st.columns(4)
        sc1.metric("Inputs", len(inputs))
        sc2.metric("Outputs", len(outputs))
        sc3.metric("Internal Wires", len(wires))
        sc4.metric("Registers", len(regs))
        
        st.markdown("---")
        st.markdown("### 🏷️ Parsed Symbol Hierarchy")
        st.json({
            "ModuleName": mod_name,
            "InputPorts": inputs,
            "OutputPorts": outputs,
            "InternalWires": wires,
            "Registers": regs,
            "Assignments": assigns
        })
