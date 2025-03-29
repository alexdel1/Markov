# -*- coding: utf-8 -*-
"""csv_to_svg_c.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LIWSL2AFA8eIry5G9Q_FwPDoXqZggv3O

!sudo apt update
!sudo apt install graphviz libgraphviz-dev
#ne pas oublier la version dev de graphviz

!pip install pygraphviz
"""

# Commented out IPython magic to ensure Python compatibility.
# 
# 
# %%capture
# !pip install git+https://github.com/alexdel1/graph_csv_to_svg.git
# !sudo apt update
# !sudo apt install graphviz libgraphviz-dev
# !pip install pygraphviz
# !pip install dot2tex
# !sudo apt install pdf2svg
# !sudo apt update
# !sudo apt install texlive-xetex

import pandas as pd
import io
import unicodedata
import re
import networkx as nx
import pygraphviz # Import the Graph class
from networkx.drawing.nx_pydot import to_pydot
from IPython.display import SVG
import subprocess
import warnings
warnings.simplefilter("ignore")
# Function to convert text to a valid Python variable name
def to_variable_name(text):
    # Normalize the text to decompose accented characters
    text = unicodedata.normalize('NFKD', str(text))

    # Remove non-ASCII characters and replace with their base letters
    text = text.encode('ascii', 'ignore').decode('ascii')

    # Remove remaining special characters and replace spaces with underscores
    text = re.sub(r'[^\w\s]', '', text)
    text = text.replace(' ', '_')

    return text


'''
(B,C)=csv_to_pd(csv_data,csv_node)

print("\nDataFrame B:")
print(B)
print("\nDataFrame C:")
print(C)
'''

def pd_to_nx(B,C):
    # Assuming B and C DataFrames are already created from the previous code

    # Create an empty graph
    G = nx.DiGraph()  # Using DiGraph for a directed graph

    # Add nodes from table B
    # Use the 'name' column as node identifier and 'texlbl' as a node attribute
    for _, row in B.iterrows():
        G.add_node(
            row['name'],  # Use the converted variable name as node identifier
            texlbl=row['texlbl'],  # Original label as a node attribute
            shape=row['shape'],
            color=row['color'],
            lblstyle=row['lblstyle'],
            style=row['style'] if 'style' in row else None  
        )

    # Add edges from table C
    for _, row in C.iterrows():
        # Add an edge using the converted source and target names
        G.add_edge(
            row['source_name'],  # Source node
            row['target_name'],  # Target node
            style=row.get('style', ''),  # Style attribute
            texlbl=row.get('label', ''),  # Label attribute
            color=row.get('color', ''),
            lblstyle=row.get('lblstyle', '')
        )
    return G
'''
G = pd_to_nx(B,C)
# Optional: Verify the graph
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

# Optional: Print node and edge details
print("\nNodes:")
for node in G.nodes(data=True):
    print(node)

print("\nEdges:")
for edge in G.edges(data=True):
    print(edge)
'''

# Convertir le graphe en pygraphviz AGraph
#A = to_agraph(G)

# Personnaliser le style
#A.graph_attr.update(rankdir="LR")  # Orientation de gauche à droite
#A.node_attr.update(fontsize="10", style="filled")
#A.edge_attr.update(color="black", arrowsize="0.5")
#A.graph_attr.update(encoding="utf-8")

# Écrire directement dans un fichier DOT
#A.write("graph.dot")

def nx_to_dot(G,tex_file_path="graph"):
    dot_graph = to_pydot(G)

    # Save the DOT file
    with open(tex_file_path+".dot", "w", encoding="utf-8") as f:
        f.write(dot_graph.to_string())
    return(dot_graph)
'''
dot_graph=nx_to_dot(G)
print(dot_graph.to_string())
'''


# Écrire directement dans un fichier DOT
#A.write("graph.dot")


'''
# Method 3: Using read().splitlines()
with open('graph.dot', 'r') as file:
    lines = file.read().splitlines()
    for line in lines:
        print(line)
# Method 3: Using read().splitlines()
with open('graph.dot', 'r') as file:
    lines = file.read().splitlines()
    for line in lines:
        print(line)
'''


def dot_to_svg(tex_file_path):
    # Using subprocess for shell commands
    subprocess.run(f'dot2tex --docpreamble "\\usepackage[utf8]{{inputenc}} \\usepackage[T1]{{fontenc}} \\usepackage{{amssymb}}" -tmath --autosize "{tex_file_path}.dot" > "{tex_file_path}.tex"', shell=True)
    insert_resizebox(f"{tex_file_path}.tex")
    subprocess.run(f'xelatex "{tex_file_path}.tex"', shell=True)

    subprocess.run(f'pdf2svg "{tex_file_path}.pdf" "{tex_file_path}.svg"', shell=True)

    SVG(f"{tex_file_path}.svg")

#dot_to_svg("graphorand")

'''
tex_file_path="graphsim"
(B,C)=csv_to_pd(csv_data,csv_node)
G = pd_to_nx(B,C)
nx_to_dot(G,tex_file_path)

!dot2tex --docpreamble "\\usepackage[utf8]{{inputenc}} \\usepackage[T1]{{fontenc}} \\usepackage{{amssymb}}" -tmath --autosize "{tex_file_path}.dot" > "{tex_file_path}.tex"
insert_resizebox(f"{tex_file_path}.tex")
!xelatex "{tex_file_path}.tex"
subprocess.run(f'pdf2svg "{tex_file_path}.pdf" "{tex_file_path}.svg"', shell=True)
SVG(f"{tex_file_path}.svg")
'''

def replace_csv_placeholders(csv_text, replacements):

    lines = csv_text.strip().split('\n')

        # Process lines, replacing placeholders
    processed_lines = []
    for line in lines:
            # Skip empty lines
            if not line.strip():
                continue

             # Replace placeholders in each line
            for key, value in replacements.items():
                line = line.replace(f'{{{key}}}', str(value))

            processed_lines.append(line)
    processed_csv = '\n'.join(processed_lines)
    return(processed_csv)



def insert_standalone(tex_file_path):
    with open(tex_file_path, 'r') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        if line.startswith(r"\documentclass{article}"):
            lines[i] = r"\documentclass[border=0pt]{standalone}" + "\n"
            break
    for i, line in enumerate(lines):
        if line.startswith(r"\enlargethispage{100cm}"):
            lines[i] = r"" + "\n"
            break


    with open(tex_file_path, 'w') as f:
        f.writelines(lines)


def test():
    print(f"ipynb version test")
#csv_to_svg(csv_data)
#csv_to_svg(csv_data,csv_node,"testor")

def csv_to_pd(csv_data,csv_node=""):
    # Create DataFrame A
    A = pd.read_csv(io.StringIO(csv_data), comment='#')
    D = ""
       # Create DataFrame B with distinct elements from first two columns
    B = pd.concat([A['source'], A['target']]).drop_duplicates()
    B = pd.DataFrame({
        'texlbl': B,
        'name': B
    })
    #print("here 1",B)
    #If a node CSV is provided, update texlbl in B with node labels
    if csv_node:
        D = pd.read_csv(io.StringIO(csv_node), comment='#')
        #print(D)
        #print(B)
        # Merge B with D to update texlbl
        B = B.merge(D[['name','style', 'texlbl','shape','color','lblstyle']], on='name', how='left')
        #print(B)
        # Update texlbl column, keeping original if no match in D
        B['texlbl'] = B['texlbl_y'].fillna(B['texlbl_x'])

        # Drop the temporary merge columns
        B = B.drop(columns=['texlbl_x', 'texlbl_y'])
        #print(B)
    #print("here2",B)
    B = pd.DataFrame({
        'texlbl': B['texlbl'],
        'name': B['name'].apply(to_variable_name),
        'shape':B['shape'],
        'color':B['color'],
        'lblstyle':B['lblstyle'],
        'style':B['style'] 
    })
    # Create DataFrame C
    #print("here3",B)
    # Create DataFrame C
    C = pd.DataFrame({
        'source_name': A['source'].apply(to_variable_name),
        'target_name': A['target'].apply(to_variable_name),
        'label': A['label'],
        'style': A.iloc[:, 3],
        'color': A['color'],
        'lblstyle' :A['lblstyle']
    })
    B['shape'].fillna("rectangle", inplace=True)
    B['color'].fillna("black", inplace=True)
    B['lblstyle'].fillna("black",inplace=True)
    C['label'].fillna("", inplace=True)
    C['style'].fillna("solid", inplace=True)
    C['color'].fillna("black", inplace=True)
    C['lblstyle'].fillna("black", inplace=True)
    return (B,C)
def csv_to_svg(csv_data,csv_node="",tex_file_path = "graph"):
    (B,C)=csv_to_pd(csv_data,csv_node)
    G = pd_to_nx(B,C)
    nx_to_dot(G,tex_file_path)


    # Using subprocess for shell commands
    subprocess.run(f'dot2tex --docpreamble "\\usepackage[utf8]{{inputenc}} \\usepackage[T1]{{fontenc}} \\usepackage{{amssymb}}" -tmath --autosize "{tex_file_path}.dot" > "{tex_file_path}.tex"', shell=True)
    insert_standalone(f"{tex_file_path}.tex")
    subprocess.run(f'xelatex "{tex_file_path}.tex"', shell=True)

    subprocess.run(f'pdf2svg "{tex_file_path}.pdf" "{tex_file_path}.svg"', shell=True)
    #print(f"ipynb version")
    display(SVG(f"{tex_file_path}.svg"))
    return G

def nx_to_svg(G,tex_file_path = "graph"):

    nx_to_dot(G,tex_file_path)


    # Using subprocess for shell commands
    subprocess.run(f'dot2tex --docpreamble "\\usepackage[utf8]{{inputenc}} \\usepackage[T1]{{fontenc}} \\usepackage{{amssymb}}" -tmath --autosize "{tex_file_path}.dot" > "{tex_file_path}.tex"', shell=True)
    insert_standalone(f"{tex_file_path}.tex")
    subprocess.run(f'xelatex "{tex_file_path}.tex"', shell=True)

    subprocess.run(f'pdf2svg "{tex_file_path}.pdf" "{tex_file_path}.svg"', shell=True)
    #print(f"ipynb version")
    display(SVG(f"{tex_file_path}.svg"))
    return G

def nx_to_svgf(G,tex_file_path = "graph"):

    nx_to_dot(G,tex_file_path)


    # Using subprocess for shell commands
    subprocess.run(f'dot2tex --docpreamble "\\usepackage[utf8]{{inputenc}} \\usepackage[T1]{{fontenc}} \\usepackage{{amssymb}}" -tmath --autosize "{tex_file_path}.dot" > "{tex_file_path}.tex"', shell=True)
    insert_standalone(f"{tex_file_path}.tex")
    subprocess.run(f'xelatex "{tex_file_path}.tex"', shell=True)

    subprocess.run(f'pdf2svg "{tex_file_path}.pdf" "{tex_file_path}.svg"', shell=True)
    #print(f"ipynb version")
    #display(SVG(f"{tex_file_path}.svg"))
    return G



'''
(B,C)=csv_to_pd(csv_data,csv_node)
print("here B",B)
print("here C",C)
tex_file_path=display(B)
G = pd_to_nx(B,C)
tex_file_path="teststandalone"
nx_to_dot(G,tex_file_path)
!dot2tex --docpreamble "\\usepackage[utf8]{{inputenc}} \\usepackage[T1]{{fontenc}} \\usepackage{{amssymb}}" -tmath --autosize "{tex_file_path}.dot" > "{tex_file_path}.tex"
insert_standalone(f"{tex_file_path}.tex")
!xelatex "{tex_file_path}.tex"
subprocess.run(f'pdf2svg "{tex_file_path}.pdf" "{tex_file_path}.svg"', shell=True)
SVG(f"{tex_file_path}.svg")#csv_to_svg(csv_data,csv_node,"teststandalone")
'''

# Parse the CSV data
csv_data = r"""source,target,label,style,color,lblstyle
éq.,classe éq.,3.1.7,,{week1},{week1}
deg. 1,irr.,3.1.16,{week1},{week1}
éq. déc.,déc.,3.1.23,,{week1},{week1}
éq. irr.,irr.,3.1.24,,{week1},{week1}
éq. comp. réd.,comp. réd.,3.1.25,,{week1},{week1}
unit.,irr. ou déc.2,3.2.3,,{week2},{week2}
éq. unit.,éq. irr. ou éq. déc.,éq. 3.2.3,,{week2},{week2}
éq. irr. ou éq. déc.,éq. irr.,,,{week2},{week2}
éq. irr. ou éq. déc.,éq. déc.,,,{week2},{week2}
fini,éq. unit.,3.2.4,,{week2},{week2}
fini,irr. ou déc.1,3.2.5,,{week2},{week2}
irr. ou déc.1,irr.,,,{week2},{week2}
irr. ou déc.1,déc.,,,{week2},{week2}
irr. ou déc.2,irr.,,,{week2},{week2}
irr. ou déc.2,déc.,,,{week2},{week2}
irr.,indéc.,3.2.7 pas la réciproque,,{week2},{week2}
irr.,irr. ou déc.3,,dashed,{week2},{week2}
déc.,irr. ou déc.3,,dashed,{week2},{week2}
irr. ou déc.3,fini et irr. ou déc.3,,dashed,{week2},{week2}
fini,fini et irr. ou déc.3,,,{week2},{week2}
fini et irr. ou déc.3,comp. réd.,3.2.8 Th. Maschke,,{week2},{week2}
irr.,phirhoirr.,,,{week3},{week3}
phirhoirr.,phirho irr.,,,{week3},{week3}
phirho irr. et phinsimrho,homgphirho0,4.1.6 Lemme Schur,,{week3},{week3}
phirho irr. et phisimrho,homgphirho1,4.1.6 Lemme Schur,,{week3},{week3}
phirho irr. et phiegalrho,Thomothetie,4.1.6 Lemme Schur,,{week3},{week3}
phirho irr.,phirho irr. et phinsimrho,,,{week3},{week3}
phinsimrho,phirho irr. et phinsimrho,,,{week3},{week3}
phirho irr.,phirho irr. et phisimrho,,,{week3},{week3}
phisimrho,phirho irr. et phisimrho,,,{week3},{week3}
phirho irr.,phirho irr. et phiegalrho,,,{week3},{week3}
phiegalrho,phirho irr. et phiegalrho,,,{week3},{week3}
groupe,groupe et commutatif,,,{week3},{week3}
commutatif,groupe et commutatif,,,{week3},{week3}
groupe et commutatif,abélien,,,{week3},{week3}
abélien,abélien et irr.,,,{week3},{week3}
irr.,abélien et irr.,,,{week3},{week3}
abélien et irr.,deg. 1,4.1.8,,{week3},{week3}
abélien,abélien et fini,,,{week3},{week3}
fini,abélien et fini,,,{week3},{week3}
abélien et fini,diag.,4.1.9,,{week3},{week3}
fini,fini et phinsimrho et phirho irr. et unit.,,,{week4},{week4}
phinsimrho,fini et phinsimrho et phirho irr. et unit.,,,{week4},{week4}
phirho irr.,fini et phinsimrho et phirho irr. et unit.,,,{week4},{week4}
unit.,fini et phinsimrho et phirho irr. et unit.,,,{week4},{week4}
fini et phinsimrho et phirho irr. et unit.,relorthoschur,4.2.8 Relations Orthogonalité Schur,,{week4},{week4}
fini,fini et classe éq. et irr.,,,{week4},{week4}
classe éq.,fini et classe éq. et irr.,,dashed,{week4},{week4}
irr.,fini et classe éq. et irr.,,dashed,{week4},{week4}
fini et classe éq. et irr.,orthosetLG,4.2.10,,{week4},{week4}
phisimrho,chiphiegalchirho,4.3.4,,{week5},{week5}
fini,fini et phirho irr.,,,{week5},{week5}
phirho irr.,fini et phirho irr.,,,{week5},{week5}
fini et phirho irr.,premrelortho,4.3.9 Première relation d'orthogonalité,,{week5},{week5}
fini,fini et phinsimrho et phirho irr.,,,{week5},{week5}
phinsimrho,fini et phinsimrho et phirho irr.,,,{week5},{week5}
phirho irr.,fini et phinsimrho et phirho irr.,,,{week5},{week5}
fini et phinsimrho et phirho irr.,phirho ortho set,4.3.9,,{week5},{week5}
fini,irr. et classe éq.,,,{week5},{week5}
#Airr.,irr. et classe éq., ,dashed,{week5},{week5}
classe éq.,irr. et classe éq., ,dashed,{week5},{week5}
comp. réd.,irr. et classe éq., ,dashed,{week5},{week5}
premrelortho,irr. et classe éq., ,dashed,{week5},{week5}
irr. et classe éq.,unique déc.,4.3.14,,{week5},{week5}
irr.,chirhochirho1,4.3.15,,{week5},{week5}
chirhochirho1,irr., ,,{week5},{week5}
rég.,unit.,4.4.2,,{week6},{week6}
fini,egalGdeg,4.4.5,,{week6},{week6}
fini,fini et orthosetLG et egalGdeg,,,{week7},{week7}
egalGdeg,fini et orthosetLG et egalGdeg,,dashed,{week7},{week7}
orthosetLG,fini et orthosetLG et egalGdeg,,dashed,{week7},{week7}
fini et orthosetLG et egalGdeg,BONLG,4.4.6,,{week7},{week7}
abélien et fini,G. éq.,4.4.9,,{week7},{week7}
G. éq.,G. éq. et fini,,,{week7},{week7}
fini,G. éq. et fini,,,{week7},{week7}
G. éq. et fini,abélien,4.4.9,,{week7},{week7}
fini,secrelortho,4.4.12 Seconde relation d'orthogonalité,,{week7},{week7}
"""

csv_node=r"""name,texlbl,shape,color,lblstyle
éq.,"$\begin{aligned}\text{équivalence 3.1.7 : }\phi \sim \rho \text{ si } \exists T \forall g \text{ tel que } \phi_g=T\rho_gT^{-1} \\ \sim \text{ est une relation d'équivalence } \end{aligned}$",,{week1},{week1}
classe éq.,"$\begin{aligned}\sim \text{ réalise une partition des représentations de groupe} \\ \text{On peut construire un ensemble des représentants: } \phi^{(1)} \,\dots \phi^{(s)} \end{aligned}$",,{week1},{week1}
fini,$\mathrm{card}(G)<\infty$,,{week1},{week1}
comp. réd.,$\phi\sim\phi^{(1)}\oplus\phi^{(2)}\dots\oplus\phi{(n)}\text{ avec }\phi^{(i)} \text{ irr .}$,,{week2},{week2}
éq. déc.,,,{week1},{week1}
déc.,,,{week1},{week1}
éq. irr.,,,{week1},{week1}
irr.,,,{week1},{week1}
éq. comp. réd.,,,{week1},{week1}
unit.,,,{week2},{week2}
éq. unit.,,,{week2},{week2}
indéc.,,,{week2},{week2}
irr. ou déc.1,$\mathrm{ou}$,diamond,{week2},{week2}
éq. irr. ou éq. déc.,$\mathrm{ou}$,diamond,{week2},{week2}
irr. ou déc.2,$\mathrm{ou}$,diamond,{week2},{week2}
irr. ou déc.3,$\mathrm{ou}$,diamond,{week2},{week2}
fini et irr. ou déc.3,$\mathrm{et}$,diamond,{week2},{week2}
phirho irr. et phinsimrho,$\mathrm{et}$,diamond,{week3},{week3}
phirho irr. et phisimrho,$\mathrm{et}$,diamond,{week3},{week3}
phirho irr. et phiegalrho,$\mathrm{et}$,diamond,{week3},{week3}
phinsimrho,$\phi\nsim\rho$,,{week3},{week3}
phisimrho,$\phi\sim\rho$,,{week3},{week3}
phinsimrho,$\phi\nsim\rho$,,{week3},{week3}
phiegalrho,$\phi = \rho$,,{week3},{week3}
homgphirho0,"$\mathrm{Hom}_G(\phi, \rho)=\{0\}$",,{week3},{week3}
homgphirho1,"$\mathrm{dim}\left(\mathrm{Hom}_G(\phi, \rho)\right)=1$",,{week3},{week3}
Thomothetie,"$\mathrm{Hom}_G(\phi, \rho)=\{\lambda I\}$",,{week3},{week3}
phi et rho,$\mathrm{et},diamond,{week3},{week3}
phirho,"$\phi,\rho$",,{week3},{week3}
phirhoirr.,"$\phi,\rho$",diamond,{week3},{week3}
phirho irr.,"$\phi,\rho\quad\mathrm{irr.}$",,{week3},{week3}
deg. 1,"$\mathrm{deg}(\phi)=1$",,{week3},{week3}
abélien et irr.,$\mathrm{et}$,diamond,{week3},{week3}
abélien,,,{week3},{week3}
groupe,,,{week3},{week3}
commutatif,,,{week3},{week3}
groupe et commutatif,$\mathrm{et}$,diamond,{week3},{week3}
abélien et fini,$\mathrm{et}$,diamond,{week3},{week3}
diag.,"$\exists T \,\forall g \quad T^{-1}\phi_gT \quad\mathrm{diagonale}$",,{week3},{week3}
fini et phinsimrho et phirho irr. et unit.,$\mathrm{et}$,diamond,{week3},{week3}
relorthoschur,"$\begin{aligned}&1. ⟨\phi_{ij},\rho_{kl}⟩ = 0 \\&2. ⟨\phi_{ij},\phi_{kl}⟩ = \begin{cases}\frac{1}{n}, & \text{si } i = k \text{ et } j = 0 \\0, & \text{sinon.}\end{cases}\end{aligned}$",,{week4},{week4}
fini et classe éq. et irr.,$\mathrm{et}$,diamond,{week4},{week4}
orthosetLG,"$\vcenter{\hbox{$\begin{array}{c}\{\sqrt{d_k}\phi^{(k)}_{ij}\vert 1 \leq k \leq s,1 \leq i, j \leq d_k\} \text{ est un ensemble orthonormal de } L(G) \\ \text{ avec } s \leq_{\text{abélien}} d_1^2 + \cdots + d_s^2 \leq_{4.4.6} |G|\end{array}$ }}$",,{week4},{week4}
chiphiegalchirho,$\chi_\phi=\chi_\rho$,,{week5},{week5}
premrelortho,"$<\chi_{\phi}, \chi_{\rho}> = \begin{cases}1, & \text{si } \phi \sim \rho \\0, & \text{si } \phi \not\sim \rho\end{cases}$",,{week5},{week5}
fini et phirho irr.,$\mathrm{et}$,diamond,{week5},{week5}
fini et phinsimrho et phirho irr.,$\mathrm{et}$,diamond,{week5},{week5}
chirhochirho1,"$<\chi_{\rho}, \chi_{\rho}> = 1$",,{week5},{week5}
phirho ortho set,"$\{\chi_\phi,\chi_\rho\}\text{ est un ensemble orthonormal de }Z(L(G))$",,{week5},{week5}
irr. et classe éq.,$\mathrm{et}$,diamond,{week5},{week5}
unique déc.,"$\vcenter{\hbox{$\begin{array}{c}\phi \sim {\phi^{(1)}}^{\oplus m_1} \oplus  {\phi^{(2)}}^{\oplus m_2} \oplus ... \oplus  {\phi^{(k)}}^{\oplus m_k} \\\text{Existence et unicité de l'équivalent au choix des représentants des classes pour les représentations irréductibles près}\end{array}$}}$",,{week5},{week5}
egalGdeg,$\vert G \vert = d_1^2+d_2^2+\cdots+d_s^2$,,{week6},{week6}
secrelortho,"$\sum_{i=1}^s \chi_i(g) \overline{\chi_i(h)} = \begin{cases} \frac{|G|}{|\overline{g}|}, & \text{si } \overline{g}=\overline{h} \\0, & \text{sinon.}\end{cases}$",,{week7},{week7}
rég.,,,{week6},{week6}
fini et orthosetLG et egalGdeg,$\mathrm{et}$,diamond,{week7},{week7}
BONLG,"$B=\{\sqrt{d_k}\phi_{ij}^{(k)} \vert 1 \leq k \leq s, 1 \leq i,j \leq d_k\}\text{ est une base orthonormée de } L(G)$",,{week7},{week7}
G. éq.,"$\left\vert \mathrm{Hom}_{irr}(G,GL(V))/{ \sim }\right\vert=|G|$",,{week7},{week7}
G. éq. et fini,$\mathrm{et}$,diamond,{week7},{week7}
"""

def graph_extract(Grep,nodeini,pre,suc,*args):

    #nodeini={"abelien"}
    #print(nodeini)
    finalnodes=set()
    finalnodes.update(nodeini)
    nodes=nodeini
    all_predecessors = set()
    #pre=2
    for _ in range(pre):
        for node in nodes:
            #print(nodes)
            all_predecessors.update(Grep.predecessors(node))
        nodes=all_predecessors.copy()

    finalnodes.update(nodes)
    nodes=nodeini
    all_successors = set()
    #suc=2
    for _ in range(suc):
        for node in nodes:
            #print(nodes)
            all_successors.update(Grep.successors(node))
        nodes=all_successors.copy()

    finalnodes.update(nodes)
    #print(finalnodes)

    addele=[]
    for ele in finalnodes:
        if Grep.nodes[ele]['shape']=="diamond":
            #print(ele)
            addele+=list(Grep.predecessors(ele))

    finalnodes.update(addele)
    #subgraph = Grep.subgraph(finalnodes)
    #nx_to_svgf(subgraph,test)
    for arg in args:

        finalnodes.update(graph_extract(Grep,*arg))
        #print(arg)
    return finalnodes

def G_E(Grep,nodeini,pre,suc,*args):
    return nx_to_svg(Grep.subgraph(graph_extract(Grep,nodeini,pre,suc,*args)))

import numpy as np

def create_array_ZnZ(n):
  """Creates an n x n array with elements exp(2*i*pi*k*m/4).

  Args:
    n: The size of the array.

  Returns:
    An n x n NumPy array.
  """

  array = np.zeros((n, n), dtype=complex)
  for k in range(n):
    for m in range(n):
      array[k, m] = np.round(np.exp(2 * np.pi * 1j * k * m / n))
  namec=['['+str(i)+']' for i in range(n)]
  table=np.vstack((namec,array))
  namer=['\\chi_'+str(i) for i in range(n)]
  table=np.hstack((np.transpose(np.concatenate(([' '],namer))).reshape(n+1, 1),table))
  return table

import numpy as np

def matrice_permutation(permutation):
    """
    Crée une matrice de permutation à partir d'une liste de permutation.

    Args:
    permutation (list): Liste représentant la permutation des indices

    Returns:
    numpy.ndarray: Matrice de permutation
    """
    n = len(permutation)
    matrice = np.zeros((n, n), dtype=int)

    for i, j in enumerate(permutation):
        matrice[i, j] = 1

    return matrice

def dataframe_to_latex_array(df):
    # Define the column format with vertical borders
    column_format = "|".join(["l"] + ["c"] * (len(df.columns) - 1))
    latex_code = f"\\begin{{array}}{{|{column_format}|}}\n"

    # Add a top border
    latex_code += "\\hline\n"

    # Add header row with borders
    latex_code += " & ".join(df.columns) + " \\\\\n\\hline\n"

    # Add data rows with borders
    for _, row in df.iterrows():
        latex_code += " & ".join(map(str, row.values)) + " \\\\\n\\hline\n"

    # Close the array
    latex_code += "\\end{array}"
    return latex_code

import numpy as np

import numpy as np

def array_to_latex(array):
    """
    Convert a NumPy array to a LaTeX array format with borders and bold first row and column.

    Parameters:
    array (np.ndarray): A 2D NumPy array to be converted to LaTeX format.

    Returns:
    str: LaTeX formatted string representing the array.
    """
    # Define the LaTeX array environment with borders
    column_format = "|c" * array.shape[1] + "|"
    latex_code = f"\\begin{{array}}{{{column_format}}}\n\\hline\n"

    # Add the first row with bold entries
    #first_row = " & ".join(f"\\mathbf{{{x}}}" for x in array[0])
    first_row = " & ".join(f"{x}" for x in array[0])
    latex_code += f"{first_row} \\\\\n\\hline\n"

    # Add the rest of the rows with the first column bold
    for row in array[1:]:
        #bold_first_col = f"\\mathbf{{{row[0]}}}"
        bold_first_col = f"{row[0]}"
        row_data = " & ".join(str(x) for x in row[1:])
        latex_code += f"{bold_first_col} & {row_data} \\\\\n\\hline\n"

    # Close the LaTeX array environment
    latex_code += "\\end{array}"
    return latex_code

def array_to_latex_with_bold(array):
    """
    Convert a NumPy array to a LaTeX array format with borders and bold first row and column.

    Parameters:
    array (np.ndarray): A 2D NumPy array to be converted to LaTeX format.

    Returns:
    str: LaTeX formatted string representing the array.
    """
    # Define the LaTeX array environment with borders
    column_format = "|c" * array.shape[1] + "|"
    latex_code = f"\\begin{{array}}{{{column_format}}}\n\\hline\n"

    # Add the first row with bold entries
    first_row = " & ".join(f"\\mathbf{{{x}}}" for x in array[0])
    #first_row = " & ".join(f"{x}" for x in array[0])
    latex_code += f"{first_row} \\\\\n\\hline\n"

    # Add the rest of the rows with the first column bold
    for row in array[1:]:
        bold_first_col = f"\\mathbf{{{row[0]}}}"
        #bold_first_col = f"{row[0]}"
        row_data = " & ".join(str(x) for x in row[1:])
        latex_code += f"{bold_first_col} & {row_data} \\\\\n\\hline\n"

    # Close the LaTeX array environment
    latex_code += "\\end{array}"
    return latex_code
