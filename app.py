import streamlit as st
import re
import graphviz

st.set_page_config(page_title="VeriVision Pro - AI RTL Visualizer & Verification Suite", page_icon="⚡", layout="wide")

# Custom Title & Header
st.title("⚡ VeriVision Pro: RTL Logic Visualizer & Static Linter")
st.caption("Advanced AI-Assisted Hardware Verification Suite & EDA Flow Assistant for Digital Engineers.")

# Sidebar Navigation & Settings
st.sidebar.header("⚙️ Control Panel")
theme_choice = st.sidebar.selectbox("Schematic Theme", ["Default Light", "High Contrast", "Blueprint"])
show_diagram = st.sidebar.checkbox("Generate RTL Schematic Diagram", value=True)
run_linter = st.sidebar.checkbox("Run Static Linting Check", value=True)

# Sample Code Library
st.sidebar.markdown("---")
st.sidebar.subheader("📚 Quick Verilog Templates")
template = st.sidebar.radio("Select Template", ["2-to-1 MUX & FlipFlop", "Simple AND Gate", "Full Adder"])

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
    sample_code = """module and_gate (\n    input wire in1,\n    input wire in2,\n    output wire out\n);\n    assign out = in1 & in2;\nendmodule"""
elif template == "Full Adder":
    sample_code = """module full_adder (\n    input wire a, b, cin,\n    output wire sum, cout\n);\n    assign sum = a ^ b ^ cin;\n    assign cout = (a & b) | (b & cin) | (a & cin);\nendmodule"""

# Code Editor Text Area
verilog_code = st.text_area(
    "📝 Paste / Edit Verilog Code Here (Press Ctrl+Enter to apply changes):", 
    value=sample_code, 
    height=240,
    key="verilog_editor"
)

# Manual Run Button & File Export
c_btn1, c_btn2 = st.columns([1, 4])
with c_btn1:
    if st.button("🚀 Analyze & Generate", type="primary"):
        st.rerun()
with c_btn2:
    st.download_button(
        label="📥 Download Verilog File (.v)",
        data=verilog_code,
        file_name="design.v",
        mime="text/x-verilog"
    )

st.markdown("---")

# --- PARSER ENGINE ---
def parse_verilog(code):
    inputs = list(dict.fromkeys(re.findall(r'input\s+(?:wire|reg)?\s*\[?\d*:?\d*\]?\s*(\w+)', code)))
    outputs = list(dict.fromkeys(re.findall(r'output\s+(?:wire|reg)?\s*\[?\d*:?\d*\]?\s*(\w+)', code)))
    wires = list(dict.fromkeys(re.findall(r'wire\s+\[?\d*:?\d*\]?\s*(\w+)', code)))
    regs = list(dict.fromkeys(re.findall(r'reg\s+\[?\d*:?\d*\]?\s*(\w+)', code)))
    assigns = re.findall(r'assign\s+(\w+)\s*=\s*([^;]+);', code)
    modules = re.findall(r'module\s+(\w+)', code)
    module_name = modules[0] if modules else "UnknownModule"
    return module_name, inputs, outputs, wires, regs, assigns

mod_name, inputs, outputs, wires, regs, assigns = parse_verilog(verilog_code)

# --- TABBED VIEW ARCHITECTURE ---
tab1, tab2, tab3 = st.tabs(["🖼️ RTL Schematic & Logic Flow", "🔍 Linter & AI Code Fixer", "📊 Hardware AST Summary"])

# TAB 1: SCHEMATIC
with tab1:
    if show_diagram and verilog_code.strip():
        dot = graphviz.Digraph(comment='Verilog RTL Flow')
        dot.attr(rankdir='LR', size='10,6')
        
        # Color Themes
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
    st.subheader(f" static Analysis for Module: `{mod_name}`")
    warnings = []
    all_declared = set(inputs + outputs + wires + regs)
    
    for var in all_declared:
        matches = len(re.findall(rf'\b{var}\b', verilog_code))
        if matches <= 1:
            warnings.append(f"Unused Signal: `{var}` is declared but never driven or referenced.")
            
    if "always @" in verilog_code and "=" in verilog_code and "<=" not in verilog_code:
        warnings.append("Coding Style Violation: Sequential `always` block detected with blocking assignment (`=`) instead of (`<=`).")
        
    if warnings:
        for w in warnings:
            st.warning(f"⚠️ {w}")
            
        st.markdown("---")
        st.subheader("💡 AI Auto-Fix Assistant Suggestion")
        st.info("The AI engine suggests removing unused signals and switching to non-blocking assignments:")
        
        # Auto-fixed code generator preview
        cleaned_code = verilog_code
        for var in all_declared:
            if len(re.findall(rf'\b{var}\b', verilog_code)) <= 1:
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
    st.markdown("### 🗂️ Parsed Symbol Hierarchy")
    st.json({
        "ModuleName": mod_name,
        "InputPorts": inputs,
        "OutputPorts": outputs,
        "InternalWires": wires,
        "Registers": regs,
        "Assignments": assigns
    })