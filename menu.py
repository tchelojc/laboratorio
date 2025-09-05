# ==============================================
# TRECHO FINAL CORRIGIDO DO menu.py
# ==============================================

# Imports Essenciais
import os
import sys
import psutil
import traceback
import qiskit
import qiskit_aer
from pathlib import Path
from typing import Dict, List, Any

# Imports Qiskit
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import Sampler
from qiskit.visualization import plot_histogram
from qiskit.utils import local_hardware_info as original_hardware_info

# Configuração do Streamlit
import streamlit as st
import matplotlib.pyplot as plt

# ==============================================
# 1. INICIALIZAÇÃO DO AMBIENTE
# ==============================================
def inicializar_ambiente():
    """Configuração inicial do ambiente quântico"""
    if 'circuito' not in st.session_state:
        qc = QuantumCircuit(2, 2)  # 2 qubits, 2 bits clássicos
        qc.h(0)
        qc.cx(0, 1)
        qc.measure_all()  # Adiciona medições automaticamente
        st.session_state.circuito = qc
        
    if 'shots' not in st.session_state:
        st.session_state.shots = 1024

    if 'quantum_validado' not in st.session_state:
        st.session_state.quantum_validado = False

    if 'historico' not in st.session_state:
        st.session_state.historico = []

# ==============================================
# 2. PATCHES DE COMPATIBILIDADE
# ==============================================
try:
    # Patch simplificado de hardware info
    def enhanced_hardware_info():
        hw_info = original_hardware_info() or {}
        hw_info['memory'] = psutil.virtual_memory().total / (1024 ** 3)
        hw_info['gpu'] = importlib.util.find_spec("cupy") is not None
        return hw_info
    
    qiskit.utils.local_hardware_info = enhanced_hardware_info

except Exception as e:
    st.error(f"Erro crítico na configuração: {str(e)}")
    sys.exit(1)

# ==============================================
# 3. FUNÇÕES PRINCIPAIS DE EXECUÇÃO
# ==============================================
def executar_experimento(shots: int):
    """Execução moderna usando Sampler"""
    try:
        # Verificação crítica adicionada
        if st.session_state.circuito.num_clbits == 0:
            st.session_state.circuito.measure_all()
            
        simulator = AerSimulator()
        transpiled_circuit = transpile(st.session_state.circuito, simulator)
        
        sampler = Sampler()
        result = sampler.run(transpiled_circuit, shots=shots).result()
        counts = result.quasi_dists[0].binary_probabilities()
        
        with st.container(border=True):  # ← Alteração crítica
            st.subheader("📊 Resultados Detalhados")
            col1, col2 = st.columns([3,1])
            with col1:
                fig = plot_histogram(counts)
                st.pyplot(fig)
            with col2:
                st.metric("Shots Executados", shots)
                st.metric("Estados Possíveis", len(counts))
                
    except Exception as e:
        st.error(f"Erro quântico: {str(e)}")
        st.code(traceback.format_exc())
        return None

# ==============================================
# 4. INTERFACE DO USUÁRIO COMPLETA
# ==============================================
def exibir_sidebar():
    """Barra lateral com controles principais"""
    with st.sidebar:
        st.header("⚙️ Navegação Principal")
        st.session_state.shots = st.slider("Número de Shots", 100, 5000, 1024)
        
        if st.button("⚡ Executar Experimento", type="primary"):
            executar_experimento(st.session_state.shots)
            
        st.divider()
        
        if st.button("🔄 Resetar Circuito"):
            st.session_state.circuito = QuantumCircuit(2, 2)  # Com bits clássicos
            st.session_state.circuito.h(0)
            st.session_state.circuito.cx(0, 1)
            st.session_state.circuito.measure_all()
            st.rerun()
            
        if st.button("📚 Ajuda Rápida"):
            mostrar_ajuda_quantica()

# ==============================================
# NO TRECHO DA FUNÇÃO exibir_terminal_quantico()
# ==============================================
def exibir_terminal_quantico():
    """Terminal interativo quântico"""
    with st.expander("💻 Terminal Quântico (Digite /help)", expanded=True):
        user_input = st.text_input("Comando:")
        if user_input:
            processar_comando(user_input)
            st.session_state.historico.append(user_input)
            
        # Substituir por:
        if st.session_state.historico:
            with st.container(border=True):  # ← Alteração crítica
                st.write("📜 Histórico de Comandos:")
                for cmd in reversed(st.session_state.historico):
                    st.code(cmd, language='bash')

def exibir_laboratorio():
    """Interface principal do laboratório"""
    col1, col2 = st.columns([1, 2])
    
    with col1:
        with st.container(border=True):
            st.header("🔧 Ferramentas Quânticas")
            if st.button("Adicionar H"):
                st.session_state.circuito.h(0)
            if st.button("Adicionar CNOT"):
                st.session_state.circuito.cx(0, 1)
            if st.button("Medir Todos"):
                st.session_state.circuito.measure_all()
                
    with col2:
        with st.container(border=True):
            st.header("🔬 Visualização do Circuito")
            st.code(st.session_state.circuito.draw(output='text'), language='text')

def processar_comando(comando: str):
    """Processador de comandos atualizado"""
    try:
        comando = comando.lower().strip()
        
        if comando == "/help":
            mostrar_ajuda_quantica()
            
        elif comando.startswith("/exemplo"):
            criar_circuito_exemplo()
            st.rerun()  # Força atualização do circuito
            
        elif comando.startswith("/quiz"):
            if "quiz_app" not in st.session_state:
                from modules.chat import QuantumQuizApp
                st.session_state.quiz_app = QuantumQuizApp()
            st.session_state.quiz_app.display_question()
            st.rerun()
            
        elif comando.startswith("/executar"):
            partes = comando.split()
            shots = int(partes[1]) if len(partes) > 1 else 1024
            executar_experimento(shots)
            
        else:
            st.warning("Comando não reconhecido. Digite /help para ajuda.")

    except Exception as e:
        st.error(f"Erro: {str(e)}")
        st.code(traceback.format_exc())
        
def criar_circuito_exemplo():
    """Cria circuito de entrelaçamento com medições"""
    qc = QuantumCircuit(2, 2)  # 2 qubits, 2 bits clássicos
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()  # Adiciona medições automaticamente
    st.session_state.circuito = qc
    st.toast("✅ Circuito exemplo criado com sucesso!", icon="⚡")

def mostrar_ajuda_quantica():
    """Sistema de ajuda interativo"""
    with st.chat_message("assistant", avatar="🦾"):
        st.markdown("""
        ## 🚀 Guia de Comandos Quânticos
        
        **Comandos Disponíveis:**
        ```bash
        /help       - Mostra este guia
        /exemplo    - Cria circuito de entrelaçamento
        /executar   - Executa o circuito (ex: /executar 1000)
        /quiz       - Inicia o quiz quântico
        ```
        
        **Portas Quânticas:**
        ```python
        circuito.h(0)    # Adiciona porta Hadamard
        circuito.cx(0,1) # Adiciona porta CNOT
        ```
        """)

def iniciar_quiz():
    """Sistema de quiz quântico integrado"""
    from modules.chat import QuantumQuizApp
    if "quiz_app" not in st.session_state:
        st.session_state.quiz_app = QuantumQuizApp()
    st.session_state.quiz_app.display_question()

# ==============================================
# 5. CONFIGURAÇÃO PRINCIPAL
# ==============================================
st.set_page_config(
    page_title="Quantum Lab 5.0",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://qiskit.org/documentation/",
        "About": f"⚛️ Qiskit {qiskit.__version__} | Aer {qiskit_aer.__version__}"
    }
)

def main():
    inicializar_ambiente()
    exibir_sidebar()
    
    st.title("🧪 Laboratório Quântico 5.0")
    exibir_laboratorio()
    exibir_terminal_quantico()
    
    with st.sidebar.expander("ℹ️ Informações do Sistema"):
        st.write(f"Qiskit: {qiskit.__version__}")
        st.write(f"Aer: {qiskit_aer.__version__}")
        st.write(f"Python: {sys.version}")

if __name__ == "__main__":
    main()