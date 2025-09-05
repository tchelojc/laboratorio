
# ==============================================
# TRECHO CORRIGIDO DO chat.py
# ==============================================

# Imports Essenciais
import sys
import os
import importlib
import qiskit  # Importação principal adicionada
from typing import Dict, List, Any
from pathlib import Path
import psutil
import platform

# Imports Qiskit 1.0.2 compatíveis
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import Sampler
from qiskit.visualization import plot_histogram
from qiskit.utils import local_hardware_info as original_hw_info

# Configuração do Streamlit
import streamlit as st

# ==============================================
# 1. CONFIGURAÇÕES INICIAIS
# ==============================================
os.environ["QISKIT_SUPPRESS_PACKAGING_WARNINGS"] = "1"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# ==============================================
# 2. VALIDAÇÃO DE AMBIENTE
# ==============================================
DEPENDENCIAS = {
    "qiskit": "1.0.2",
    "qiskit-aer": "0.13.3",
    "qiskit-ibm-provider": "0.8.0",
    "streamlit": "1.32.0",
    "numpy": "1.24.3",
    "psutil": "5.9.5",
    "matplotlib": "3.8.2"
}

def validar_ambiente_quantico():
    """Validação completa do ambiente quântico"""
    problemas = []
    solucoes = []
    
    # Verificação de hardware
    if psutil.virtual_memory().total < 8 * 1024**3:
        problemas.append("Requer mínimo de 8GB de RAM")
        solucoes.append("Atualize sua memória RAM")
    
    # Verificação de pacotes
    for pacote, versao in DEPENDENCIAS.items():
        try:
            v = importlib.metadata.version(pacote)
            if v != versao:
                problemas.append(f"{pacote} ({v}) ≠ {versao}")
                solucoes.append(f"pip install {pacote}=={versao}")
        except importlib.metadata.PackageNotFoundError:
            problemas.append(f"{pacote} não instalado")
            solucoes.append(f"pip install {pacote}=={versao}")
    
    return problemas, solucoes

# ==============================================
# 3. PATCHES DE COMPATIBILIDADE
# ==============================================
try:
    # Patch de informações de hardware
    def enhanced_hardware_info():
        hw_info = original_hw_info() or {}
        hw_info['memory'] = psutil.virtual_memory().total / (1024 ** 3)
        hw_info['gpu'] = importlib.util.find_spec("cupy") is not None
        return hw_info
    
    qiskit.utils.local_hardware_info = enhanced_hardware_info

except Exception as e:
    st.error(f"Erro crítico na configuração: {str(e)}")
    sys.exit(1)

# ==============================================
# 4. FUNÇÕES DE EXECUÇÃO QUÂNTICA
# ==============================================
def executar_experimento_quantico(shots: int):
    """Execução moderna usando Sampler do Aer"""
    try:
        if not hasattr(st.session_state, 'circuito'):
            st.error("Circuito quântico não inicializado!")
            return None
            
        # Configuração do simulador
        simulator = AerSimulator()
        
        # Transpilar circuito
        circuito_transpilado = transpile(
            st.session_state.circuito,
            simulator,
            optimization_level=3
        )
        
        # Execução quântica
        sampler = Sampler()
        resultado = sampler.run(circuito_transpilado, shots=shots).result()
        
        return resultado.quasi_dists[0].binary_probabilities()
        
    except Exception as e:
        st.error(f"Erro quântico: {str(e)}")
        st.code(traceback.format_exc())
        return None

# ==============================================
# 5. FUNÇÕES AUXILIARES
# ==============================================
def exibir_resultados_modernos(counts: dict):
    """Exibição profissional de resultados"""
    with st.expander("📊 Resultados da Simulação"):
        col1, col2 = st.columns([3,1])
        with col1:
            fig = plot_histogram(counts)
            st.pyplot(fig)
        with col2:
            st.metric("Shots Executados", st.session_state.shots)
            st.metric("Estados Possíveis", len(counts))

def inicializar_sessao():
    """Garante a inicialização correta da sessão"""
    if 'circuito' not in st.session_state:
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        st.session_state.circuito = qc

class QuantumEnvironmentValidator:
    def __init__(self):
        self.problemas = []
        self.comandos_reparo = []

    def _verificar_pacote(self, nome: str, versao: str):
        """Verificação detalhada de pacotes"""
        try:
            versao_instalada = version(nome)
            if versao_instalada != versao:
                self.problemas.append(f"{nome} ({versao_instalada}) ≠ {versao}")
                self.comandos_reparo.append(f"pip install {nome}=={versao}")
        except PackageNotFoundError:
            self.problemas.append(f"{nome} não instalado")
            self.comandos_reparo.append(f"pip install {nome}=={versao}")

    def executar_verificacao(self):
        """Executa verificação completa"""
        # Verifica ambiente virtual
        if sys.prefix == sys.base_prefix:
            self.problemas.append("Ambiente virtual não ativo")
        
        # Verifica pacotes
        for pacote, versao in DEPENDENCIAS.items():
            self._verificar_pacote(pacote, versao)
            
        return len(self.problemas) == 0

def verificar_ambiente(streamlit=False):
    """Função principal de verificação"""
    validator = QuantumEnvironmentValidator()
    sucesso = validator.executar_verificacao()
    
    if streamlit:
        st.header("🔍 Diagnóstico do Sistema")
        
        # Exibir problemas
        if validator.problemas:
            st.error("Problemas encontrados:")
            for problema in validator.problemas:
                st.write(f"- {problema}")
            
            # Sugerir reparos
            with st.expander("Comandos para correção"):
                st.code("\n".join(validator.comandos_reparo))
        else:
            st.success("✅ Ambiente validado com sucesso!")
            st.balloons()
    
    return sucesso

# ✅ MOTOR DE CRIATIVIDADE QUÂNTICA
class QuantumCreativityEngine:
    """Sistema aprimorado com tratamento de erros e validação"""
    
    def __init__(self):
        self.circuit = QuantumCircuit(2)
        self._check_packaging_first()
        self.reality_fabric = None
        self._validate_quantum_tools()
        
    def _translate_dream(self, dream_input: str) -> QuantumCircuit:
        """Cria circuito quântico baseado na entrada"""
        circuit = QuantumCircuit(2)
        circuit.h(0)
        circuit.cx(0, 1)
        return circuit  # Retorna o objeto QuantumCircuit
    
    def _check_packaging_first(self):
        """Garante o packaging antes de qualquer verificação"""
        try:
            import packaging.version
        except ImportError:
            st.warning("📦 Instalando dependência crítica...")
            subprocess.run([sys.executable, "-m", "pip", "install", "packaging==23.2"], check=True)
            st.rerun()
    
    def _validate_quantum_tools(self):
        """Validação interna dos componentes quânticos"""
        required_gates = ['cx', 'h', 'x', 'xx_plus_yy']
        try:
            self.simulator = AerSimulator()
            test_circuit = QuantumCircuit(2)
            
            for gate in required_gates:
                if gate == 'xx_plus_yy':
                    test_circuit.append(XXPlusYYGate(theta=0.5), [0, 1])
                else:
                    getattr(test_circuit, gate)(0)
            
            transpile(test_circuit, self.simulator)
            
        except Exception as e:
            st.error(f"🔧 Falha na validação de portas quânticas: {str(e)}")
            st.stop()
    
    def _translate_dream(self, dream_input: str) -> QuantumCircuit:
        """Conversão validada de linguagem natural para QASM"""
        try:
            qasm_script = self._quantum_nlp(dream_input)
            return QuantumCircuit.from_qasm_str(qasm_script)
        except Exception as e:
            st.error(f"🌀 Erro na interpretação quântica: {str(e)}")
            st.code(traceback.format_exc(), language='python')
            st.stop()
    
    def _quantum_nlp(self, text: str) -> str:
        """Gerador de QASM com validação sintática"""
        gate_map = {
            "entrelaçar": "cx q[%d], q[%d];",
            "superpor": "h q[%d];",
            "rodopiar": "x q[%d];"
        }
        
        qasm_lines = ["OPENQASM 2.0;", "include \"qelib1.inc\";", 
                     "qreg q[2];", "creg c[2];"]
        
        for idx, word in enumerate(text.split()):
            gate_template = gate_map.get(word.lower(), "h q[%d];")
            target = idx % 2
            qasm_lines.append(gate_template % target)
        
        qasm_script = "\n".join(qasm_lines)
        
        # Validação do QASM gerado
        try:
            QuantumCircuit.from_qasm_str(qasm_script)
            return qasm_script
        except Exception as e:
            st.error(f"⚡ QASM inválido gerado: {str(e)}")
            st.code(qasm_script, language='qasm')
            st.stop()
    
class SessionStateManager:
    def init_session(self, defaults: dict):
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value

    def get_state(self, key: str, default=None):
        return st.session_state.get(key, default)
    
    def update_state(self, key: str, value):
        st.session_state[key] = value
    
class ProtocolManager:
    def __init__(self):
        self.stages = {
            1: "Contextualização Dinâmica",
            2: "Análise Heurística Modular",
            3: "Preservação Adaptativa",
            4: "Iteração Assistida"
        }
        self.current_context = {}
        
    def execute_flow(self, user_input, content=None):
        # Etapa 1 - Contexto
        self._build_context(user_input, content)
        
        # Etapa 2 - Análise
        analysis = self._heuristic_analysis()
        
        # Etapa 3 - Preservação
        self._preserve_core_logic()
        
        # Etapa 4 - Iteração
        return self._generate_interactive_response(analysis)

    def _heuristic_analysis(self):
        # Implementação da análise por blocos
        return {
            'code_blocks': self._chunk_analysis(),
            'patterns': self._detect_patterns(),
            'optimization_points': self._find_optimizations()
        }
    
class QuantumErrorHandler:
    def __init__(self):
        self.session_manager = SessionStateManager()

    def _parse_error_line(self, trace):
        """Analisa detalhes do erro para highlight preciso"""
        error_lines = [line for line in trace.split('\n') if 'File "<string>"' in line]
        if error_lines:
            line_info = error_lines[0].split('line ')[1].split(',')[0]
            return int(line_info) - 1  # Ajuste para índice 0-based
        return 0

    def _display_error_details(self, error, line_num, code):    
        poetic_errors = {
            'AttributeError': "🕳️ O atributo fugiu para um buraco de minhoca!",
            'TypeError': "🌀 Tipos se entrelaçaram de forma inesperada"
        }
        
        msg = poetic_errors.get(type(error).__name__, "🌌 O desconhecido surgiu")
        st.error(f"""
        {msg}
        ```python
        {type(error).__name__}: {str(error)}
        ```
        """)
        st.image("quantum_error_art.png")  # Adicione imagens criativas
        
        """Exibe detalhes do erro com highlight avançado"""
        error_msg = f"""
        ❌ **Erro de Execução**
        ```python
        {type(error).__name__}: {str(error)}
        ```
        **Linha problemática:**
        ```python
        {self._get_error_context(code, line_num)}
        ```
        **Soluções sugeridas:**
        {self._get_error_solutions(type(error).__name__)}
        """
        
        self.session_manager.update_state('editor_errors', [{
            "row": line_num,
            "column": 0,
            "type": "error",
            "text": f"{type(error).__name__}: {str(error)}"
        }])
        
        st.error(error_msg)
        st.button("🔄 Tentar Novamente", 
                on_click=lambda: self.session_manager.update_state('editor_errors', []))  # PARÊNTESES FECHADOS

    def _get_error_context(self, code, line_num):
        """Retorna contexto do erro com highlight"""
        lines = code.split('\n')
        start = max(0, line_num - 2)
        end = min(len(lines), line_num + 3)
    
        context = []
        for i in range(start, end):
            prefix = "👉 " if i == line_num else "   "
            context.append(f"{i+1:03d} {prefix}{lines[i]}")
    
        return "\n".join(context)

    def _get_error_solutions(self, error_type):
        """Retorna soluções contextualizadas"""
        solutions = {
            'AttributeError': [
                "Verifique se todos os módulos estão importados corretamente",
                "Confira a documentação da classe/método utilizado"
            ],
            'QiskitError': [
                "Verifique a compatibilidade do circuito com o backend",
                "Use transpile() com configurações de otimização adequadas"
            ]
        }
        return "\n".join([f"- {s}" for s in solutions.get(error_type, ["Consulte a documentação oficial"])])
        
    def mostrar_terminal():
        handler = QuantumErrorHandler()
        protocol = QuantumInteractionProtocol()
        st.header("💻 Terminal Quântico Pro")

        # Ambiente de execução seguro
        safe_env = {
            '__builtins__': __builtins__,
            'QuantumCircuit': QuantumCircuit,
            'Aer': Aer,
            'transpile': transpile,
            'plot_histogram': plot_histogram,
            'plt': plt,
            'np': np,
            'st': st,
            'qc': st.session_state.get('current_circuit', QuantumCircuit(2))
        }

        # Editor de código com recursos avançados
        code = st_ace(
            key='quantum_terminal_v2',
            language='python',
            theme='dracula',
            height=500,
            font_size=14,
            wrap=True,
            annotations=st.session_state.get('editor_errors', [])
        )

        if st.button("▶ Executar no Terminal Quântico"):
            try:
                with st.spinner("🧪 Executando Código Quântico..."):
                    response = protocol.apply_protocol(code)
                
                    if response.get('validation_passed'):
                        local_vars = {'circuit': None}
                        exec(code, safe_env, local_vars)

                        if local_vars.get('circuit'):
                            st.session_state.current_circuit = local_vars['circuit']
                            st.success("✅ Circuito atualizado e pronto para execução!")

                        handler.session_manager.update_state('editor_errors', [])
                    else:
                        display_quantum_errors(response.get('analysis', {}))
                        show_repair_options(response.get('suggestions', []))

            except Exception as e:
                trace = traceback.format_exc()
                error_line = handler._parse_error_line(trace)
                handler._display_error_details(e, error_line, code)

        # Seção de Missões Quânticas
        with st.expander("🚀 Missões Quânticas", expanded=True):
            st.markdown("### Missões Disponíveis")
            st.write("1. Criar circuito entrelaçado")
            st.write("2. Executar 100 shots no simulador")
            if st.button("Atualizar Progresso"):
                st.info("📊 Progresso atualizado com sucesso!")
                
    def processar_comando(comando: str):
        """Processador de comandos integrado com o QuantumAssistantPro"""
        from modules.chat import QuantumAssistantPro
    
        if 'assistant' not in st.session_state:
            st.session_state.assistant = QuantumAssistantPro()
    
        try:
            # Processa o comando usando o assistente
            response = st.session_state.assistant.process_command(comando)
        
            # Exibe a resposta formatada
            with st.chat_message("assistant"):
                if "```" in response:
                    st.markdown(response)
                else:
                    st.info(response)
                
        except Exception as e:
            st.error(f"Erro quântico: {str(e)}")
            st.code(traceback.format_exc())
    
class QuantumAssistantPro(SessionStateManager):
    def __init__(self):
        super().__init__()
        self.creative_engine = QuantumCreativityEngine()
        self.command_registry = {}  # Inicialização obrigatória
        self._init_command_system()
        self._init_session()
        self.project_path = Path(self.get_state('project_path', str(Path.cwd()))) 

    def _init_command_system(self):
        """Sistema de comandos seguro e validado"""
        self.command_registry = {
            'projeto': self._handle_project,
            'dependencia': self._handle_dependencies,
            'init': self._handle_init,
            'executar': self._handle_execution,
            'ajuda': self._show_help,  # ADICIONADA VÍRGULA FALTANTE
            'sonhar': self._handle_creative_command,
            'manifestar': self._handle_reality_shift
        }  # FECHAMENTO CORRETO DO DICIONÁRIO

    def _init_session(self):
        """Inicialização validada da sessão"""
        self.init_session({
            'chat_history': [],
            'project_path': str(Path.cwd()),
            'current_circuit': None,
            'quantum_missions': []
        })
        
        # Novas missões quânticas
        self.quantum_missions = {
            'advanced': [
                {
                    "name": "⚛️ Entrelaçamento em Hardware Real",
                    "objective": "Executar circuito entrelaçado no IBM Quantum",
                    "validation": self._validate_hardware_execution,
                    "reward": {"points": 300, "badge": "🔭"}
                },
                {
                    "name": "🌀 Otimização de Circuito",
                    "objective": "Transpilar circuito com nível máximo de otimização",
                    "validation": self._validate_circuit_optimization,
                    "reward": {"points": 150, "badge": "⚡"}
                }
            ]
        }
        
    def _validate_circuit_optimization(self):
        """Validação de otimização de circuito"""
        try:
            qc = st.session_state.current_circuit
            if not qc:
                return {"success": False, "message": "Nenhum circuito carregado"}
        
            optimized = transpile(qc, optimization_level=3)
            return {
                "success": optimized.depth() < qc.depth(),
                "message": f"Otimização reduzida de {qc.depth()} para {optimized.depth()} camadas"
            }
        except Exception as e:
            return {"success": False, "message": f"Erro na otimização: {str(e)}"}

    def _enhanced_terminal_execution(self, code: str):
        """Execução aprimorada com análise em tempo real"""
        with st.expander("🔍 Análise Dinâmica", expanded=True):
            st.write("📊 Métricas do Código:")
        
            # Análise estática
            analysis = self._perform_quantum_analysis(code)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Circuitos Quânticos", len(analysis['quantum_circuits']))
            with col2:
                st.metric("Importações Qiskit", len(analysis['qiskit_imports']))
            with col3:
                st.metric("Linhas de Código", len(code.split('\n')))

        # Execução interativa
        with st.spinner("🌀 Executando em Núvem Quântica..."):
            try:
                local_vars = {'circuit': None}
                exec(code, self.safe_env, local_vars)
            
                if local_vars.get('circuit'):
                    st.session_state.current_circuit = local_vars['circuit']
                    self._show_circuit_actions()
                
            except Exception as e:
                self._display_error_details(e, self._parse_error_line(traceback.format_exc()), code)

    def _handle_creative_command(self, params):
        """Processa comandos de criação quântica"""
        dream = params.get('args', [''])[0]
        try:
            qc = self.creative_engine._translate_dream(dream)
            st.session_state.current_circuit = qc
            return f"🌀 Circuito dos Sonhos Criado!\n{self._show_quantum_poem(qc)}"
        except Exception as e:
            return f"❌ Falha na materialização: {str(e)}"

    def _show_quantum_poem(self, qc):
        """Exibe o circuito como poesia quântica"""
        poem = [
            "🌌 **Manifestação Quântica**",
            f"Qubits: {qc.num_qubits} Estrelas",
            f"Operações: {len(qc)} Passos Cósmicos",
            "```\n" + "\n".join(f"🌀 {op.name} q[{qubit}]" 
                              for op, qubits, _ in qc.data
                              for qubit in qubits) + "\n```"
        ]
        return "\n".join(poem)
    
    def _show_circuit_actions(self):
        """Ações pós-execução do circuito"""
        with st.container():
            st.success("✅ Execução Completa!")
            cols = st.columns(3)
        
            with cols[0]:
                if st.button("📊 Visualizar Circuito", key=f"viz_{uuid4()}"):
                    self._display_quantum_circuit()
        
            with cols[1]:
                if st.button("⚡ Otimizar", key=f"opt_{uuid4()}"):
                    self._optimize_circuit()
        
            with cols[2]:
                if st.button("🔄 Executar Novamente", key=f"rerun_{uuid4()}"):
                    st.rerun()

    def _display_quantum_circuit(self):
        """Exibição adaptada à realidade escolhida"""
        qc = st.session_state.current_circuit
        reality = self.get_state('quantum_reality', 'base')
        
        if reality == 'poética':
            st.markdown(self._show_quantum_poem(qc))
        elif reality == 'fractal':
            self._draw_fractal_circuit(qc)
        else:
            super()._display_quantum_circuit()

    def _draw_fractal_circuit(self, qc):
        """Renderização artística do circuito"""
        fig = go.Figure(data=[
            go.Scatterternary(
                mode='markers+lines',
                a=[op[0] for op in qc],
                b=[op[1] for op in qc],
                marker=dict(size=20, color='rgb(158,154,200)')
            )
        ])
        st.plotly_chart(fig)
        
    def _handle_mission(self, params):
        """Sistema de missões aprimorado"""
        mission_id = params.get('args', [''])[0]
        
        if mission_id == "listar":
            return self._list_missions()
            
        return self._start_mission(mission_id)

    def _list_missions(self):
        """Lista missões disponíveis com status"""
        mission_list = []
        for level, missions in self.quantum_missions.items():
            mission_list.append(f"## 🌟 {level.capitalize()}")
            for idx, mission in enumerate(missions):
                status = "✅" if mission.get('completed') else "⚡"
                mission_list.append(f"{idx+1}. {status} {mission['name']} - {mission['objective']}")
        
        return "\n".join(mission_list)

    def _start_mission(self, mission_id):
        """Inicia e valida uma missão"""
        mission = next((m for m in self.quantum_missions['advanced'] if m['name'] == mission_id), None)
        
        if not mission:
            return "Missão não encontrada. Use !missao listar"
            
        validation_result = mission['validation']()
        if validation_result['success']:
            self._award_mission(mission)
            return f"🎉 Missão completa! {validation_result['message']}"
            
        return f"❌ Missão falhou: {validation_result['message']}"

    def _validate_hardware_execution(self):
        """Valida execução em hardware real"""
        try:
            job = self._execute_on_hardware(st.session_state.current_circuit)
            return {
                "success": job.status() == 'DONE',
                "message": f"Job {job.job_id()} executado no IBM Quantum!"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Erro: {str(e)}"
            }

    def _handle_share(self, params):
        """Compartilha circuito no IBM Quantum Composer"""
        qc = st.session_state.current_circuit
        if not qc:
            return "⚠️ Nenhum circuito carregado!"
            
        try:
            composer_link = self._generate_composer_link(qc)
            webbrowser.open_new_tab(composer_link)
            return f"🔗 Circuito compartilhado: [Abrir no Composer]({composer_link})"
        except Exception as e:
            return f"❌ Erro ao compartilhar: {str(e)}"

    def _generate_composer_link(self, qc: QuantumCircuit):
        """Gera link direto para o Quantum Composer"""
        qasm = qc.qasm()
        base64_qasm = base64.b64encode(qasm.encode()).decode()
        return f"https://quantum-computing.ibm.com/composer/?qasm={base64_qasm}"

    def _handle_hardware(self, params):
        """Gerencia execução em hardware real"""
        operation = params.get('args', ['status'])[0]
        
        operations = {
            'listar': self._list_ibm_devices,
            'executar': self._run_on_hardware
        }
        
        return operations.get(operation, lambda: "Operação inválida")()

    def _list_ibm_devices(self):
        """Lista dispositivos IBM disponíveis"""
        provider = IBMProvider()
        backends = provider.backends()
        
        device_list = ["## 🖥️ IBM Quantum Devices"]
        for backend in backends:
            status = "✅ Online" if backend.status().operational else "⛔ Offline"
            device_list.append(f"- {backend.name} ({backend.num_qubits} qubits) {status}")
        
        return "\n".join(device_list)

    def _run_on_hardware(self):
        """Executa circuito atual no hardware"""
        qc = st.session_state.current_circuit
        if not qc:
            return "⚠️ Nenhum circuito para executar!"
            
        try:
            job = self._execute_on_hardware(qc)
            return f"""
            🚀 Job enviado com sucesso!
            - ID: {job.job_id()}
            - Status: {job.status()}
            - Posição na fila: {job.queue_position()}
            """
        except Exception as e:
            return f"❌ Falha na execução: {str(e)}"

    def _show_activation(self):
        """Mostra instruções de ativação do ambiente virtual"""
        activation = self._get_activation_command()
        return f"""
        🔌 Ambiente Virtual:
        ```bash
        {activation}
        ```
        Execute este comando no seu terminal para ativar o ambiente
        """

    def _get_activation_command(self):
        """Retorna o comando correto para o SO"""
        return "source quantum_env/bin/activate" if sys.platform != "win32" else r".\quantum_env\Scripts\activate"

    def _quantum_surgery(self, params):
        """Executor de operações estruturais com engrenagem quântica"""
        operation = params.get('operation', 'venv')
        
        operations = {
            'venv': self._create_quantum_venv,
            'ativar': self._show_activation,
            'reorganizar': self._reorganize_structure,
            'autoinit': self._auto_init,
            'diagnostico': self._system_diagnostic  # Novo diagnóstico
        }
        return operations.get(operation, lambda: "Operação inválida")()

    def _handle_project(self, params):
        """Implementação completa da criação de projetos"""
        try:
            project_name = params.get('name', 'novo_projeto')
            with st.status(f"🧬 Criando projeto {project_name}..."):
                st.write("📂 Gerando estrutura de pastas...")
                time.sleep(0.5)
                
                # Cria estrutura básica
                base_structure = [
                    'circuitos',
                    'dados',
                    'analise',
                    'main.py'
                ]
                
                for item in base_structure:
                    (self.project_path / item).mkdir(parents=True, exist_ok=True)
                
                return f"""
                ✅ **Projeto {project_name} criado!**
                ```bash
                cd {project_name}
                !cirurgiao ativar
                !executar main.py
                ```
                """
        except Exception as e:
            return f"❌ Erro na criação: {str(e)}"

    def process_command(self, user_input: str):
        protocol = QuantumInteractionProtocol()
        response = protocol.apply_protocol(user_input)
        
        self._display_interactive_response(response)
        self._update_state_based_on_analysis(response)

    def _display_interactive_response(self, response):
        """Exibe resposta seguindo o protocolo"""
        with st.chat_message("assistant"):
            st.markdown(f"## {response['summary']}")
            
            # Bloco de Análise
            with st.expander("🧩 Análise Modular", expanded=True):
                for block in response['analysis_blocks']:
                    st.markdown(f"### {block['title']}")
                    st.json(block['details'])
            
            # Ações Sugeridas
            st.markdown("### 🚀 Ações Recomendadas")
            for action in response['action_steps']:
                if st.button(action['label'], help=action['tooltip']):
                    self.execute_action(action['command'])

    def _update_chat_history(self, command: str, response: str):
        """Atualiza o histórico do chat"""
        history = self.get_state('chat_history', [])
        history.extend([
            {'role': 'user', 'content': command},
            {'role': 'assistant', 'content': response}
        ])
        self.update_state('chat_history', history)

    def _guide_project_creation(self, text: str) -> str:
        """Guia interativo para criação de projetos"""
        return """
        🚀 Guia de Criação de Projetos:
        
        1. Comece com:
        ```bash
        !projeto quantico --name nome_do_projeto
        ```
        
        2. Ative o ambiente virtual:
        ```bash
        !cirurgiao ativar
        ```
        
        3. Instale dependências:
        ```bash
        !dependencia --auto
        ```
        """

    def _parse_params(self, params: list) -> dict:
        """Analisa parâmetros de comando complexos"""
        parsed = {'args': [], 'flags': {}}
        for param in params:
            if param.startswith('--'):
                key_value = param[2:].split('=', 1)
                parsed['flags'][key_value[0]] = key_value[1] if len(key_value) > 1 else True
            else:
                parsed['args'].append(param)
        return parsed

    def _log_command_execution(self, command: str, response: str):
        """Registra execução de comandos no histórico"""
        self.update_state('chat_history', [
            *self.get_state('chat_history'),
            {'role': 'user', 'content': command},
            {'role': 'assistant', 'content': response}
        ])

    def _handle_entities(self, params: Dict) -> str:
        """Gestão quântica de entidades"""
        operation = params.get('operation', 'listar')
        
        operations = {
            'criar': self._criar_entidade,
            'listar': self._listar_entidades,
            'editar': self._editar_entidade
        }
        
        if operation not in operations:
            return "⚠️ Operação inválida. Use: criar, listar ou editar"
            
        return operations[operation](params)

    def _criar_entidade(self, params: Dict) -> str:
        """Cria nova entidade através do GenericEntityManager"""
        try:
            entity_manager = GenericEntityManager(
                entity_name=params.get('tipo', 'entidade'),
                fields=[
                    {'name': 'nome', 'type': 'text', 'required': True},
                    {'name': 'tipo', 'type': 'select', 'options': ['qubit', 'gate', 'circuit']}
                ],
                options={'icon': '🔮', 'color': '#8e44ad'}
            )
            entity_manager.entity_form()
            return "✅ Entidade quântica criada com sucesso!"
        
        except Exception as e:
            self._log_error(str(e))
            return f"❌ Erro na criação: {str(e)}"

    def _listar_entidades(self, params: Dict) -> str:
        """Lista entidades existentes"""
        entity_type = params.get('tipo', 'entidade')
        entity_manager = GenericEntityManager(entity_name=entity_type, fields=[])
        entity_manager.display_entities()
        return f"📋 Listando entidades do tipo: {entity_type}"

    def _editar_entidade(self, params: Dict) -> str:
        """Edição quântica de entidades existentes"""
        entity_id = params.get('id')
        if not entity_id:
            return "⚠️ ID da entidade não especificado"
            
        # Lógica de edição seria implementada aqui
        return f"✏️ Editando entidade quântica ID: {entity_id}"
                
    def _show_development_flow(self, params):
        """Fluxo cirúrgico completo com comandos executáveis"""
        flow = """
        🌌 **Fluxo de Desenvolvimento Quântico**

        1. 🗂️ Criar Estrutura Básica
        ```bash
        !projeto quantico --name meu_experimento
        ```
        
        2. 🏗️ Configurar Ambiente Virtual
        ```bash
        !cirurgiao venv  # Cria ambiente
        !cirurgiao ativar  # Ativa com:
        source quantum_env/bin/activate  # Linux/Mac
        quantum_env\\Scripts\\activate  # Windows
        ```
        
        3. 🧩 Gerar Estrutura de Módulos
        ```bash
        !init --auto  # Cria portais quânticos
        ```
        
        4. 🤖 Desenvolver com IA Assistida
        ```bash
        !gerar circuito --qbits 2  # Exemplo
        !gerar otimizador --camadas 3
        ```
        
        5. 📦 Gerenciar Dependências
        ```bash
        !dependencia --auto  # Detecta e instala
        ```
        
        6. 🔄 Atualização Contínua
        ```bash
        !cirurgiao reorganizar  # Regera estrutura
        ```
        """
        return flow
    
    def _reorganize_structure(self):
        """Reorganização automática da estrutura do projeto"""
        try:
            self._auto_init()
            self._handle_dependencies({'auto': True})
            self._generate_project_map()
            return "🔄 Estrutura reorganizada com sucesso!\nSistema atualizado:"
        
        except Exception as e:
            self._log_error(str(e))
            return f"❌ Falha na reorganização: {str(e)}"
    
    def _generate_project_map(self):
        """Gera mapa de dependências quânticas"""
        structure = self._analyze_project_structure()
        dependency_map = self._detect_missing_dependencies()
        
        map_content = f"""
        🌌 Mapa Quântico do Projeto
        
        **Estrutura:**
        {json.dumps(structure, indent=2)}
        
        **Dependências:**
        {json.dumps(dependency_map, indent=2)}
        """
        
        map_file = self.project_path / 'quantum_map.md'
        map_file.write_text(map_content)
        
    def _system_diagnostic(self):
        """Diagnóstico completo do sistema"""
        diagnostics = {
            'estrutura': self._analyze_project_structure(),
            'dependencias': self._detect_missing_dependencies(),
            'erros': self._read_error_log(),
            'performance': self._check_performance()
        }
        
        return f"📊 Diagnóstico do Sistema:\n```json\n{json.dumps(diagnostics, indent=2)}\n```"

    def _natural_language_response(self, user_input: str) -> str:
        """Resposta inteligente para comandos naturais"""
        responses = {
            'ajuda': self._show_help,
            'projeto': lambda: "Use !projeto [tipo] para criar novos projetos",
            'erro': lambda: "Verifique o log com !erro"
        }
        
        for keyword, response in responses.items():
            if keyword in user_input.lower():
                return response()
        
        return "🔍 Comando não reconhecido. Digite !ajuda para opções."

    def _show_help(self, params):
        """Sistema de ajuda quântico atualizado"""
        help_text = """
        🌌 **Sistema de Ajuda Quântica**
    
        **Comandos Principais:**
        ```bash
        !entidade [operaçao]  # Gerencia entidades (criar, listar, editar)
        !projeto [tipo]  # Tipos: simples, quantico, plataforma
        !dependencia          # Gerencia pacotes Python
        !executar [arquivo.py]  # Executa código quântico
        !init --auto  # Cria estrutura de módulos
        !init                 # Cria portais entre módulos
        !executar             # Roda código quântico
        !ajuda          # Mostra esta ajuda
        ```
    
        **Exemplo Completo:**
        ```bash
        !projeto quantico --name meuexperimento
        !dependencia --auto
        !executar circuitos/entrelacamento.py
        !entidade criar --tipo qubit
        !entidade listar --tipo gate
        ```
        # Instala dependências
        !dependencia --auto
        
        # Executa circuito principal
        !executar circuitos/entrelacamento.py
        ```
        """
        
        return help_text

    def _unknown_command(self, params):
        """Manipula comandos desconhecidos com explicação quântica"""
        return f"🌀 Comando não reconhecido. Comandos disponíveis:\n{', '.join(self.command_registry.keys())}"

    def _handle_code_analysis(self, params: Dict) -> str:
        """Análise quântica de código (Lições 6 e 7)"""
        try:    
            code_path = self.project_path / params.get('arquivo', 'main.py')
        
            if not code_path.exists():
                return f"⚠️ Arquivo não encontrado: {code_path}"

            with code_path.open('r', encoding='utf-8') as f:
                code_content = f.read()
            
            analysis = self._perform_quantum_analysis(code_content)
            return f"🔍 Análise Completa:\n```python\n{analysis}\n```"
        
        except Exception as e:
            self._log_error(str(e))
            return f"❌ Falha na análise: {str(e)}"

    def _perform_quantum_analysis(self, code: str) -> Dict:
        """Executa análise estática quântica"""
        tree = ast.parse(code)
    
        analysis_results = {
            'qiskit_imports': [],
            'quantum_circuits': [],
            'potential_errors': []
        }
    
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and 'qiskit' in node.module:
                    analysis_results['qiskit_imports'].append(node.module)
                
            if isinstance(node, ast.ClassDef):
                if any(isinstance(base, ast.Name) and base.id == 'QuantumCircuit' for base in node.bases):
                    analysis_results['quantum_circuits'].append(node.name)
                
        return analysis_results

    def _init_command_system(self):
        """Sistema de comandos quânticos aprendido durante nossa jornada"""
        self.command_registry = {
            'iniciar': self._iniciar_projeto,
            'projeto': self._handle_project,
            'dependencia': self._handle_dependencies,
            'init': self._handle_init,
            'codigo': self._handle_code_analysis,
            'executar': self._handle_execution,
            'ambiente': self._handle_environment,
            'erro': self._handle_errors
        }

        self.help_system = {
            'projeto': self._project_help,
            'dependencia': self._dependency_help,
            'init': self._init_help,
            'padrao': self._default_help
        }
        
    def _iniciar_projeto(self, params):
        """Fluxo de iniciação rápida de projeto"""
        try:
            self._handle_project({'type': 'quantico', 'name': 'novo_projeto'})
            self._handle_dependencies({'auto': True})
            self._handle_init({'auto': True})
            return "🚀 Projeto iniciado com sucesso!\nEstrutura completa pronta para desenvolvimento."
        except Exception as e:
            return f"❌ Falha na iniciação: {str(e)}"

    def _display_response(self, response: str, is_code: bool = False):
        """Exibe respostas ricas com formatação quântica"""
        with st.chat_message("assistant", avatar="🦾"):
            if "```" in response:
                parts = response.split("```")
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        st.write(part)
                    else:
                        lang = part.split("\n")[0] if "\n" in part else ""
                        code = "\n".join(part.split("\n")[1:]) if "\n" in part else part
                        st.code(code, language=lang if lang else "python")
            else:
                st.write(response)
            
            # Adiciona ações pós-resposta
            with st.expander("📌 Ações Recomendadas"):
                if "circuito" in response:
                    st.button("🧬 Visualizar Circuito", key=f"viz_{uuid4()}")
                    st.button("⚡ Otimizar Parâmetros", key=f"opt_{uuid4()}")
                elif "erro" in response.lower():
                    st.button("🛠️ Auto-correção", key=f"fix_{uuid4()}")

        self._update_history('assistant', response)

    def _update_history(self, role: str, content: str):
        """Atualiza o histórico diretamente no session_state"""
        st.session_state.chat_history.append({
            'role': role,
            'content': content
        })

    def _analyze_project_structure(self):
        """Análise quântica de projetos - Lição 1"""
        structure = {
            'pastas': [],
            'arquivos_python': [],
            'requerimentos': []
        }

        for path in self.project_path.rglob('*'):
            if path.is_dir():
                if path.name not in {'__pycache__', 'venv'}:
                    structure['pastas'].append(str(path.relative_to(self.project_path)))
            elif path.suffix == '.py':
                structure['arquivos_python'].append(path.name)
        
        return structure

    def _post_project_setup(self, project_type: str):
        """Pós-processamento aprendido com erros passados"""
        if project_type == 'quantico':
            self._generate_quantum_init()
            self._install_dependencies(['qiskit', 'numpy'])

    def _generate_quantum_init_content(self, folder_path: Path) -> str:
        """Gera conteúdo inicial para arquivos quânticos"""
        # Garante que o Path seja convertido para string
        path_str = str(folder_path.resolve())
        relative_path = folder_path.relative_to(self.project_path)
        imports = []
    
        # Adiciona imports relativos
        for f in folder_path.glob('*.py'):
            if f.stem != '__init__':
                imports.append(f"from . import {f.stem}")
    
        # Adiciona dependências detectadas
        for dep in self._detect_missing_dependencies()['missing']:
            imports.append(f"# 🔍 Pacote necessário: {dep}")
    
        # Corrigindo a f-string problemática
        imports_str = '\n'.join(imports)  # Primeiro junta os imports
    
        return (
            f"# 🌌 Portal Quântico Automático\n"
            f"# 📍 {relative_path.as_posix()}\n\n"  # Caminho seguro
            f"{imports_str}\n\n"  # Usa a string já formatada
            f"__all__ = {[f.stem for f in folder_path.glob('*.py') if f.stem != '__init__']}"
        )
        return template_content
        
    def _handle_dependencies(self, params: Dict):
        """Gestão de dependências com detecção quântica - Versão Corrigida"""
        auto_mode = params.get('auto', False)
    
        if auto_mode:
            detected = self._detect_missing_dependencies()
            if detected['missing']:
                self._install_dependencies(detected['missing'])
        
            self._freeze_requirements()
            return (
                f"📦 Dependências atualizadas!\n"
                f"Instalados: {', '.join(detected['missing'])}\n"
                f"Requirements atualizado em {self.project_path/'requirements.txt'}"
            )
        return "⚠️ Modo automático não ativado. Use !dependencia --auto"

    def _detect_missing_dependencies(self):
        """Detecção de dependências baseada em imports - Lição 4"""
        required = {'qiskit', 'numpy', 'streamlit'}
        installed = {pkg.key for pkg in pkg_resources.working_set}
        
        return {
            'missing': list(required - installed),
            'installed': list(installed)
        }

    def _handle_init(self, params: Dict):
        """Criação de inits com comunicação quântica"""
        try:
            structure = self._analyze_project_structure()
            for folder in structure['pastas']:
                init_file = self.project_path / folder / '__init__.py'
                if not init_file.exists():
                    content = self._generate_init_content(folder)
                    init_file.write_text(content)
                    
            return f"🧩 {len(structure['pastas'])} portais quânticos criados!"

        except Exception as e:
            self._log_error(str(e))
            return f"❌ Erro nos inits: {str(e)}"

    def _generate_init_content(self, folder: str) -> str:
        """Geração de conteúdo aprendida com erros"""
        imports = [
            "# 🌌 Portal gerado automaticamente",
            f"# Caminho: {folder}",
            "\n# Conexões quânticas"
        ]
        
        # Adiciona imports relativos
        py_files = list((self.project_path / folder).glob('*.py'))
        for f in py_files:
            if f.stem != '__init__':
                imports.append(f"from . import {f.stem}")

        # Adiciona dependências globais
        imports.append("\n# Dependências universais")
        for req in self._detect_missing_dependencies()['installed']:
            imports.append(f"import {req}")

        return '\n'.join(imports)

    def _handle_execution(self, params: Dict) -> str:
        """Execução quântica com verificação (Lição 8)"""
        try:
            file_to_run = self.project_path / params.get('arquivo', 'main.py')
            result = subprocess.run(
                ['python', str(file_to_run)],
                capture_output=True,
                text=True
            )
        
            if result.returncode != 0:
                error_msg = f"Erro na execução:\n{result.stderr}"
                self._log_error(error_msg)
                return f"❌ Falha:\n```\n{error_msg}\n```"
            
            return f"⚡ Executado com sucesso!\nSaída:\n```\n{result.stdout}\n```"

        except Exception as e:
            self._log_error(str(e))
            return f"❌ Erro crítico: {str(e)}"

    def _handle_errors(self, params: Dict) -> str:
        """Gestão de erros aprendida (Lição 9)"""
        error_log = self.project_path / 'quantum_errors.log'
    
        if not error_log.exists():
            return "✅ Nenhum erro registrado"
        
        errors = error_log.read_text()
        return f"📜 Histórico de Erros:\n```\n{errors}\n```"

    def _log_error(self, error_msg: str):
        """Gestão de erros com verificação de diretório"""
        error_dir = self.project_path / 'quantum_logs'
        error_dir.mkdir(exist_ok=True)  # Cria diretório se não existir
    
        error_log = error_dir / 'errors.log'
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        with error_log.open('a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {error_msg}\n")

    def _handle_environment(self, params: Dict):
        """Gestão de ambientes virtuais - Lição 5"""
        env_cmd = "python -m venv quantum_env"
        activation = (
            "source quantum_env/bin/activate" if sys.platform != "win32" 
            else "quantum_env\\Scripts\\activate"
        )
        
        try:
            subprocess.run(env_cmd, shell=True, check=True)
            return f"🌍 Ambiente criado!\nAtive com:\n```\n{activation}\n```"
        except subprocess.CalledProcessError:
            return "⚠️ Erro ao criar ambiente. Verifique permissões."

    def _execute_example_flow(self):
        """Fluxo completo de exemplo com feedback visual"""
        progress_bar = st.progress(0)
        status_text = st.empty()
    
        steps = [
            ("Criando projeto...", self._handle_project, {'type': 'quantico', 'name': 'meuexperimento'}),
            ("Instalando dependências...", self._handle_dependencies, {'auto': True}),
            ("Gerando estrutura...", self._handle_init, {'auto': True}),
            ("Preparando ambiente...", self._create_quantum_venv, {})
        ]
    
        for i, (msg, func, params) in enumerate(steps):
            progress_bar.progress((i+1)/len(steps))
            status_text.markdown(f"🚀 **{msg}**")
            time.sleep(0.5)
            result = func(params)
        
        return "✅ Fluxo completo executado! Projeto pronto em /meuexperimento"

    def _natural_language_processing(self, text: str) -> str:
        """NLP básico baseado em nosso histórico"""
        text = text.lower()
    
        if any(word in text for word in ['ajuda', 'help']):
            return self._show_help({})
    
        if 'projeto' in text:
            return self._guide_project_creation(text)
        
        return "🤔 Comando não reconhecido. Tente '!ajuda' para opções."

    def _project_help(self) -> str:
        return """
        🌀 **Ajuda para Projetos**  
        Comandos disponíveis:  
        ```
        !projeto [tipo]  
        Tipos válidos: simples, quantico, plataforma, startup  
        Exemplo: !projeto quantico  
        ```
        """

    def _dependency_help(self) -> str:
        return """
        📦 **Gestão de Dependências**  
        Comandos:  
        ```
        !dependencia instalar [pacotes]  
        !dependencia atualizar  
        Exemplo: !dependencia instalar qiskit numpy  
        ```
        """
        
    def _init_help(self) -> str:
        """Sistema de ajuda para criação de inits quânticos"""
        return """
        🧩 **Ajuda para Portais Quânticos (__init__)**

        Comandos disponíveis:
        ```bash
        !init criar       # Cria inits em todas as pastas
        !init verificar   # Lista portais faltantes
        ```

        Exemplo completo:
        ```bash
        !init criar --path meus_modulos
        ```
        """

    def _default_help(self) -> str:
        """Ajuda geral para comandos desconhecidos"""
        return """
        🆘 **Ajuda Geral do Sistema Quântico**
        Comandos principais:
        ```bash
        !projeto     # Gestão de projetos
        !dependencia # Controle de pacotes
        !init        # Portais entre módulos
        !executar    # Rodar códigos
        ```

        Digite `!ajuda [comando]` para detalhes
        """
        
    def _show_development_flow(self, params):
        """Exibe o fluxo completo de desenvolvimento quântico"""
        flow = """
        🌌 **Fluxo de Desenvolvimento Quântico Cirúrgico**

        1. 🗂️ **Criação de Estrutura**
        ```bash
        !projeto quantico --name meu_experimento
        ```
        
        2. 🏗️ **Ambiente Virtual Quântico**
        ```bash
        !cirurgiao venv  # Cria ambiente virtual
        !cirurgiao ativar  # Ativa o ambiente
        ```
        
        3. 🧬 **Gestão de Módulos**
        ```bash
        !init --auto  # Cria __init__.py inteligentes
        ```
        
        4. 🤖 **Desenvolvimento com IA**
        ```bash
        !gerar circuito_entrelacamento --qbits 2
        ```
        
        5. 📦 **Gestão de Dependências**
        ```bash
        !dependencia --auto  # Detecta e instala requisitos
        ```
        
        6. 🔄 **Modificação Contínua**
        ```bash
        !cirurgiao reorganizar  # Regera estrutura após mudanças
        ```
        """
        return flow

    def _create_quantum_venv(self):
        """Cria ambiente virtual com dependências quânticas"""
        venv_path = self.project_path / 'quantum_env'
        venv_path.mkdir(exist_ok=True)
        
        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
            return f"✅ Ambiente virtual criado em: {venv_path}\nAtive com:\n```\n!cirurgiao ativar\n```"
        except subprocess.CalledProcessError as e:
            return f"❌ Erro ao criar ambiente: {str(e)}"

    def _activate_venv(self):
        """Ativa o ambiente virtual"""
        activation = (
            "source quantum_env/bin/activate" if sys.platform != "win32" 
            else "quantum_env\\Scripts\\activate"
        )
        return f"🌍 Ambiente ativado! Execute:\n```\n{activation}\n```"

    def _auto_init(self):
        """Cria inits com propagação quântica"""
        init_count = 0
        for path in self.project_path.rglob('*/'):
            if path.is_dir() and not (path / '__init__.py').exists():
                content = self._generate_quantum_init_content(path)
                (path / '__init__.py').write_text(content)
                init_count += 1
                
        return f"🧩 {init_count} portais quânticos criados!"

    def _install_dependencies(self, packages: List[str]):
        """Instalação quântica de pacotes"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", *packages],
                check=True,
                capture_output=True,
                text=True  # Adicionado para obter saída como string
            )
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if isinstance(e.stderr, str) else e.stderr.decode('utf-8', errors='replace')
            self._log_error(f"Erro na instalação: {error_msg}")

    def _generate_with_ai(self, params):
        """Geração de código com propagação automática"""
        component_type = params.get('component', '')
        components = {
            'circuito': self._generate_circuit_code,
            'otimizador': self._generate_optimizer,
            'entidade': self._generate_entity_code
        }
        
        if component_type not in components:
            return "⚠️ Tipo de componente inválido. Use: " + ", ".join(components.keys())
        
        generated_code = components[component_type](params)
        self._propagate_changes(component_type)
        return generated_code

    def _generate_quantum_circuit(self, params):
        """Gera código de circuito quântico"""
        qbits = params.get('qbits', 2)
        return (
            "⚡ **Circuito Quântico Gerado**\n"
            "```python\n"
            f"from qiskit import QuantumCircuit\n\n"
            f"qc = QuantumCircuit({qbits})\n"
            f"qc.h(0)\n"
            f"qc.cx(0, 1)\n"
            f"qc.measure_all()\n"
            "```\n"
            "📝 **Dica:** Modifique com portas quânticas usando:\n"
            "- qc.x() : Porta X\n"
            "- qc.h() : Porta Hadamard\n"
            "- qc.cx() : Porta CNOT"
        )
        
    def _propagate_changes(self, component_type: str):
        """Propagação quântica de mudanças"""
        self._handle_init({'auto': True})
        self._handle_dependencies({'auto': True})
        
        if component_type == 'entidade':
            self._update_entity_registry()

    def _update_entity_registry(self):
        """Atualização automática do registro de entidades"""
        entity_manager = GenericEntityManager("entidade", [])
        entity_manager._auto_init()
        return "🔄 Registro de entidades atualizado!"
    
    def _generate_error_response(self, error: Exception) -> str:
        """Gera uma resposta de erro formatada com informações úteis"""
        error_type = error.__class__.__name__
        error_msg = f"""
        ❌ **Erro Quântico Detectado**
        
        **Tipo:** `{error_type}`
        **Mensagem:** {str(error)}
        
        🔧 **Ações Recomendadas:**
        1. Verifique a sintaxe do comando
        2. Use `!ajuda` para referências
        3. Execute `!erro` para detalhes técnicos
        """
        
        self._log_error(f"{error_type}: {str(error)}")
        return error_msg
    
class QuantumCodeScanner:
    def __init__(self, full_code):
        self.lines = full_code.split('\n')
        self.chunks = self._create_quantum_chunks()
        
    def _create_quantum_chunks(self):
        # Divide o código em blocos quânticos (não lineares)
        return [self.lines[i:i+100] for i in range(0, len(self.lines), 100)]
    
    def parallel_analysis(self):
        results = {}
        for idx, chunk in enumerate(self.chunks):
            results[f'chunk_{idx}'] = {
                'metrics': self._calculate_complexity(chunk),
                'smells': self._detect_smells(chunk),
                'security': self._check_vulnerabilities(chunk)
            }
        return self._quantum_entangle(results)  # Correlaciona resultados

    def _quantum_entangle(self, data):
        # Implementação de correlação quântica entre blocos
        entangled_data = {}
        # ... (Lógica avançada de cross-analysis)
        return entangled_data
    
    def dimensional_analysis(code_chunk):
        # Redução dimensional para análise complexa
        from sklearn.decomposition import PCA
        vectorized_code = vectorize(code_chunk)
        pca = PCA(n_components=3)
        return pca.fit_transform(vectorized_code)

class QuantumQuizzer(SessionStateManager):
    def __init__(self):
        super().__init__()
        self.quizzes = self._load_quizzes()
        self._init_quiz_session()

    def _init_quiz_session(self):
        """Inicialização robusta do estado do quiz"""
        quiz_defaults = {
            'quiz_progress': 0,
            'quiz_score': 0,
            'current_question_key': 0,
            'quiz_history': []
        }
        self.init_session(quiz_defaults)

    def display_interface(self):
        """Interface interativa com tratamento de erros"""
        self._validate_session_state()
        
        if self.get_state('quiz_progress') >= len(self.quizzes):
            self._show_final_results()
            return

        current_q = self.quizzes[self.get_state('quiz_progress')]
        
        with st.container():
            st.markdown(f"### 🌀 Pergunta {self.get_state('quiz_progress') + 1}/{len(self.quizzes)}")
            st.markdown(f"**{current_q['question']}**")
            
            # Geração segura de chaves únicas
            for idx, option in enumerate(current_q['options']):
                btn_key = f"q{self.get_state('current_question_key')}_opt{idx}_{uuid4().hex[:6]}"
                if st.button(option, key=btn_key):
                    self._handle_answer(idx, current_q)
                    st.rerun()
            
            self._show_feedback()

    def _show_enhanced_feedback(self, answer):
        """Feedback detalhado com guia de solução"""
        with st.expander("📘 Feedback da Resposta", expanded=True):
            if answer['selected'] == answer['correct']:
                st.success("✅ **Resposta Correta!**")
                st.balloons()
            else:
                st.error("❌ **Resposta Incorreta**")
                correct_answer = self.quizzes[answer['question_index']]['options'][answer['correct']]
                st.markdown(f"**Resposta Correta:** `{correct_answer}`")
                
            st.markdown("### 🧠 Explicação Detalhada")
            st.markdown(answer['explanation'])
            
            # Guia passo-a-passo
            st.markdown("### 🛠️ Guia de Implementação")
            self._display_solution_steps(answer['question_index'])
            
            # Console interativo
            if st.button("🖥️ Abrir Terminal para Testar", key=f"term_{uuid4()}"):
                self._open_quantum_terminal(answer['question_index'])

    def _display_solution_steps(self, question_index):
        """Exibe passos para implementação da solução"""
        solution = {
            0: [
                "1. Use o comando: `!projeto quantico --nome [NOME]`",
                "2. Navegue até a pasta: `cd [NOME]`",
                "3. Inicie o ambiente: `!cirurgiao ativar`"
            ],
            1: [
                "1. Execute: `!cirurgiao venv`",
                "2. Ative o ambiente conforme seu SO:",
                "   - Linux/Mac: `source quantum_env/bin/activate`",
                "   - Windows: `quantum_env\\Scripts\\activate`"
            ]
        }
        
        for step in solution.get(question_index, []):
            st.write(step)

    def _open_quantum_terminal(self, question_index):
        """Prepara o terminal com exemplos relevantes"""
        examples = {
            0: "!projeto quantico --nome meu_primeiro_circuito",
            1: "!cirurgiao venv\n!cirurgiao ativar"
        }
        st.session_state.terminal_code = examples.get(question_index, "")
        st.session_state.modo_operacao = "🧠 Assistente Quântico"
        st.rerun()

# Função get_ibm_backend atualizada
    def get_ibm_backend():
        """Obtém backend local para simulações"""
        return Aer.get_backend('qasm_simulator')

    # Função de execução local corrigida
    def _execute_on_hardware(self, qc: QuantumCircuit):
        """Executa circuito localmente"""
        backend = AerSimulator()  # Usando o simulador atualizado
        return execute(qc, backend, shots=1024)

    def _get_practical_example(self, answer):
        """Mapeamento de exemplos válidos"""
        examples = {
            "projeto quantico": "!projeto quantico --name meu_experimento",
            "cirurgiao venv": "!cirurgiao venv",
            "init --auto": "!init --auto"
        }
        return examples.get(answer['explanation'].split()[-1], "Exemplo não disponível")

    def _check_answer(self, selected_idx, question):
        """Processa respostas com feedback detalhado"""
        is_correct = selected_idx == question['correct']
        new_progress = self.get_state('quiz_progress') + 1
        
        self.update_state('quiz_progress', new_progress)
        self.update_state('quiz_score', self.get_state('quiz_score') + (1 if is_correct else 0))
        
        # Registrar histórico
        new_history = self.get_state('quiz_history') + [{
            'question': question['question'],
            'selected': selected_idx,
            'correct': question['correct'],
            'explanation': question['explanation']
        }]
        self.update_state('quiz_history', new_history)

    def _show_question_feedback(self, answer):
        """Exibe explicação detalhada com exemplo executável"""
        with st.expander("📘 Feedback da Resposta", expanded=True):
            if answer['selected'] == answer['correct']:
                st.success("✅ **Resposta Correta!**")
            else:
                st.error("❌ **Resposta Incorreta**")
                
            st.markdown(f"**Explicação:** {answer['explanation']}")
            
            # Mostrar exemplo de comando relacionado
            st.markdown("**Exemplo Prático:**")
            example = self._get_practical_example(answer['explanation'])
            st.code(example, language='bash')
            
            if st.button("🔄 Tentar Comando", key=f"ex_{uuid4()}"):
                self._execute_example_command(example)

    def _execute_example_command(self, command):
        """Preenche o chat com o comando exemplo"""
        st.session_state.chat_input = command.strip().split('\n')[0]
        st.rerun()

    def _show_final_results(self):
        """Exibe resultados finais com análise detalhada"""
        st.balloons()
        score = self.get_state('quiz_score')
        total = len(self.quizzes)
        
        st.markdown(f"""
        ## 🏆 Resultado Final
        **Pontuação:** {score}/{total} ({score/total:.0%})
        """)
        
        if st.button("🔁 Refazer Quiz"):
            self._init_session()
            st.rerun()
        
    def _load_quizzes(self):
        """Perguntas com explicações detalhadas"""
        return [
            {
                "question": "🗂️ Como criar estrutura de pastas?",
                "options": [
                    "!projeto simples",
                    "!projeto quantico",
                    "!novo projeto"
                ],
                "correct": 1,
                "explanation": "Cria estrutura básica para projetos quânticos",
                "example": "!projeto quantico --name meu_experimento\n# Cria pastas: /circuitos, /dados, /analise"
                    "✅ Correto! Use:\n```bash\n!projeto quantico --name experimento\n```\n"
                    "Isso cria:\n"
                    "- /circuitos\n- /dados\n- /analise\n- main.py\n"
                    "💡 Dica: Adicione módulos com `!init --auto`"
        
            },
            {
                "question": "🏗️ Como criar ambiente virtual?",
                "options": [
                    "!cirurgiao venv",
                    "!ambiente criar",
                    "!projeto venv"
                ],
                "correct": 0,
                "explanation": (
                    "🌟 Certo! Execute:\n```bash\n!cirurgiao venv\n```\n"
                    "Depois ative:\n"
                    "Linux/Mac:\n```source quantum_env/bin/activate```\n"
                    "Windows:\n```quantum_env\\Scripts\\activate```"
                )
            },
            {
                "question": "🗂️ Primeiro passo para criar um projeto quântico?",
                "options": [
                    "Criar arquivos .py",
                    "Definir estrutura de pastas",
                    "Instalar dependências"
                ],
                "correct": 1,
                "explanation": (
                    "✅ Correto! Primeiro devemos criar a estrutura:\n"
                    "```bash\n"
                    "!projeto quantico --name meuexperimento\n"
                    "```\n"
                    "Isso cria:\n"
                    "- /circuitos\n"
                    "- /dados\n"
                    "- /analise\n"
                    "- main.py\n"
                )
            },
            {
                "question": "🏗️ Como criar um ambiente virtual?",
                "options": [
                    "!cirurgiao venv",
                    "!ambiente criar",
                    "!projeto venv"
                ],
                "correct": 0,
                "explanation": (
                    "🌟 Certo! O comando cirúrgico:\n"
                    "```bash\n"
                    "!cirurgiao venv\n"
                    "```\n"
                    "Cria a pasta quantum_env com:\n"
                    "- Interpretador Python isolado\n"
                    "- Gestão de dependências local\n"
                )
            },
            {
                "question": "🧬 Como gerar __init__.py automáticos?",
                "options": [
                    "!init --auto",
                    "Modificar manualmente",
                    "!gerar inits"
                ],
                "correct": 0,
                "explanation": (
                    "🚀 Perfeito! O comando:\n"
                    "```bash\n"
                    "!init --auto\n"
                    "```\n"
                    "Gera automaticamente:\n"
                    "- Portais quânticos entre módulos\n"
                    "- Imports relativos inteligentes\n"
                    "- Documentação básica\n"
                )
            },
            {
                "question": "🤖 Como pedir ajuda à IA para código?",
                "options": [
                    "!gerar circuito",
                    "Escrever manualmente",
                    "Copiar da internet"
                ],
                "correct": 0,
                "explanation": (
                    "💡 Use:\n"
                    "```bash\n"
                    "!gerar circuito --qbits 3\n"
                    "```\n"
                    "A IA irá criar:\n"
                    "- Estrutura básica do circuito\n"
                    "- Portas quânticas recomendadas\n"
                    "- Medições e visualização\n"
                )
            },  # VÍRGULA AQUI
            {
                "question": "🌀 Como iniciar um novo projeto quântico?",
                "options": [
                    "!novo_projeto quantico",
                    "!projeto --tipo quantum",
                    "!projeto quantico"
                ],
                "correct": 2,
                "explanation": "✅ Correto! Use `!projeto quantico` para criar um novo projeto de computação quântica."
            },
            {
                "question": "📦 Qual comando gerencia dependências?",
                "options": [
                    "!pacotes instalar",
                    "!dependencia",
                    "!instalar python"
                ],
                "correct": 1,
                "explanation": "🌟 Exato! O comando `!dependencia` cuida de todos os pacotes necessários."
            },
            {
                "question": "⚡ Como executar código quântico?",
                "options": [
                    "!rodar programa",
                    "!executar main.py",
                    "!run quantum"
                ],
                "correct": 1,
                "explanation": "🚀 Perfeito! `!executar` seguido do nome do arquivo inicia a simulação."
            },
            {
                "question": "⚙️ Como corrigir erros de estrutura?",
                "options": [
                    "!cirurgiao reorganizar",
                    "Reiniciar o projeto",
                    "Modificar manualmente"
                ],
                "correct": 0,
                "explanation": (
                    "✅ Correto! O comando:\n```bash\n!cirurgiao reorganizar\n```\n"
                    "Executa:\n1. Atualização de imports\n2. Verificação de dependências\n3. Geração de documentação"
                )
            },
            {
                "question": "🔧 Como verificar a saúde do sistema?",
                "options": [
                    "!cirurgiao diagnostico",
                    "Ler todos os logs",
                    "Reinstalar tudo"
                ],
                "correct": 0,
                "explanation": (
                    "🌟 Certo! Use:\n```bash\n!cirurgiao diagnostico\n```\n"
                    "Obtendo:\n- Status da estrutura\n- Dependências faltantes\n- Histórico de erros\n- Métricas"
                )
            }
        ]

    def _validate_session_state(self):
        """Garante a integridade do session state"""
        required_keys = [
            'quiz_progress', 
            'quiz_score',
            'current_question_key',
            'quiz_history'
        ]
        
        for key in required_keys:
            if key not in st.session_state:
                self._init_session()
                break
            
def main():
    st.title("⚛️ Simulador Quântico Certificado")
    
    with st.expander("🌠 Laboratório de Realidades Quânticas", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            dream_input = st.text_area("Escreva seu sonho quântico:")
            if st.button("Materializar Sonho"):
                response = assistant.process_command(f"!sonhar {dream_input}")
                st.write(response)
        
        with col2:
            reality = st.selectbox("Escolha sua realidade:", 
                                ['base', 'poética', 'fractal', 'entrelaçada'])
            if st.button("Ativar Realidade"):
                st.write(assistant.process_command(f"!manifestar {reality}"))

    # Editor de código quântico
    with st.expander("📟 Terminal Quântico", expanded=True):
        code = st_ace(
            language='python',
            theme='dracula',
            key='quantum_code',
            height=300
        )

    # Controles de execução
    if st.button("▶️ Executar no Simulador", type="primary"):
        try:
            qc = QuantumCircuit(2, 2)
            qc.h(0)
            qc.cx(0, 1)
            qc.measure([0, 1], [0, 1])

            simulator = Aer.get_backend('qasm_simulator')
            compiled_circuit = transpile(qc, simulator)
            job = execute(qc, simulator, shots=1000)
            result = job.result()
            counts = result.get_counts()

            st.subheader("📊 Resultados da Simulação")
            fig = go.Figure(data=[
                go.Bar(x=list(counts.keys()), y=list(counts.values()))
            ])
            st.plotly_chart(fig)

        except Exception as e:
            st.error(f"Erro Quântico: {str(e)}")
            st.code(traceback.format_exc(), language='python')

    # Inicia a interface do quiz
    if "quiz_app" not in st.session_state:
        st.session_state.quiz_app = QuantumQuizApp()

    st.session_state.quiz_app.display_question()
    

# ------------------------
# Classe do Quiz Quântico
# ------------------------
class QuantumQuizApp:
    def __init__(self):
        self.questions = [
            {
                "pergunta": "Qual porta cria superposição?",
                "opcoes": ["X", "H", "CNOT", "Z"],
                "correta": 1
            },
            {
                "question": "Qual é a porta usada para criar superposição?",
                "options": ["X", "Z", "H", "CNOT"],
                "correct": 2,
                "explanation": "A porta H (Hadamard) cria superposição em um qubit.",
                "example": "qc.h(0)"
            },
            {
                "question": "Qual porta cria emaranhamento entre dois qubits?",
                "options": ["H", "CX", "T", "Z"],
                "correct": 1,
                "explanation": "A porta CX (CNOT) pode gerar emaranhamento entre dois qubits.",
                "example": "qc.cx(0,1)"
            }
        ]
        self.current_question = 0
        
    def display_question(self):
        """Exibe a questão atual com Streamlit"""
        with st.container(border=True):
            q = self.questions[self.current_question]
            st.subheader(f"Questão {self.current_question+1}")
            st.write(q["pergunta"])
            
            for idx, opcao in enumerate(q["opcoes"]):
                if st.button(opcao, key=f"q{self.current_question}_op{idx}"):
                    self.verificar_resposta(idx == q["correta"])
            
    def _create_question_button(self, idx, option, question):
        btn_key = f"q{st.session_state.current_question_key}_opt{idx}"
        if st.button(option, key=btn_key):
            self._handle_answer(idx, question)
            st.rerun()

    def _handle_answer(self, selected_idx, question):
        """Processamento seguro de respostas"""
        is_correct = selected_idx == question['correct']
        new_state = {
            'quiz_progress': self.get_state('quiz_progress') + 1,
            'quiz_score': self.get_state('quiz_score') + (1 if is_correct else 0),
            'current_question_key': self.get_state('current_question_key') + 1,
            'quiz_history': [
                *self.get_state('quiz_history'),
                {
                    'question': question['question'],
                    'selected': selected_idx,
                    'correct': question['correct'],
                    'explanation': question['explanation']
                }
            ]
        }
        for key, value in new_state.items():
            self.update_state(key, value)

    def _show_current_question(self):
        if st.session_state.quiz_progress >= len(self.quizzes):
            st.success("🎉 Quiz Finalizado!")
            st.info(self._get_performance_message(
                st.session_state.quiz_score, len(self.quizzes)
            ))
            self._show_scoreboard()
            return

        current_q = self.quizzes[st.session_state.quiz_progress]

        with st.container():
            st.subheader(f"🌀 Pergunta {st.session_state.quiz_progress + 1}/{len(self.quizzes)}")
            st.markdown(f"**{current_q['question']}**")

            cols = st.columns(2)
            for idx, option in enumerate(current_q['options']):
                with cols[idx % 2]:
                    self._create_question_button(idx, option, current_q)

    def _show_scoreboard(self):
        st.metric("📊 Pontuação", st.session_state.quiz_score)
        st.metric("🔮 Progresso", f"{st.session_state.quiz_progress}/{len(self.quizzes)}")
        if st.button("🔄 Reiniciar Quiz"):
            self._reset_quiz()
            st.rerun()

    def _reset_quiz(self):
        st.session_state.quiz_progress = 0
        st.session_state.quiz_score = 0
        st.session_state.current_question_key = 0

    def _get_performance_message(self, score, total):
        ratio = score / total
        if ratio == 1:
            return "🌟 Domínio Quântico Total!"
        elif ratio >= 0.75:
            return "🚀 Excelente! Quase lá!"
        elif ratio >= 0.5:
            return "💡 Bom trabalho! Continue explorando!"
        else:
            return "🌌 Continue praticando! O quantum espera por você!"

    def _render_question(self, protocol_response):
        """Renderização usando o protocolo"""
        with st.container():
            # Cabeçalho Contextual
            st.markdown(f"### {protocol_response['context_summary']}")
            
            # Questão Modular
            for block in protocol_response['question_blocks']:
                self._render_question_block(block)
            
            # Feedback Adaptativo
            if protocol_response['show_feedback']:
                self._display_enhanced_feedback(protocol_response['analysis'])

    def _init_quantum_state(self):
        if 'quantum_state' not in st.session_state:
            st.session_state.quantum_state = {
                'superposition': False,
                'entanglement': [],
                'observed': False
            }

    def _show_quantum_scoreboard(self):
        st.metric("📊 Pontuação", st.session_state.quiz_score)
        st.metric("🔮 Progresso", f"{st.session_state.quiz_progress}/{len(self.quizzes)}")
        if st.button("🎩 Modo Quântico"):
            st.session_state.quantum_state['superposition'] = not st.session_state.quantum_state['superposition']
            st.rerun()

    def _show_detailed_feedback(self, question, selected_idx):
        """Feedback completo com exemplo executável"""
        correct_answer = question['options'][question['correct']]
        
        with st.expander("📘 Explicação Detalhada", expanded=True):
            st.markdown(f"**Resposta Correta:** `{correct_answer}`")
            st.markdown(question['explanation'])
            
            if 'example' in question:
                st.markdown("**Exemplo Prático:**")
                st.code(question['example'], language='bash')
                
            if st.button("▶️ Executar Comando", key=f"ex_{uuid4()}"):
                self._execute_correct_command(correct_answer)
                
    def _execute_correct_command(self, command: str):
        """Preenche automaticamente o chat com o comando correto"""
        st.session_state.chat_input = f"!{command}"
        st.rerun()
        
        if st.button("🔄 Reiniciar Quiz"):
            st.session_state.quiz_progress = 0
            st.session_state.quiz_score = 0
            st.rerun()
            
    def verificar_resposta(self, correta: bool):
        """Exibe feedback da resposta"""
        if correta:
            st.success("✅ Correto! +10 pontos quânticos")
            self.current_question = min(self.current_question+1, len(self.questions)-1)
        else:
            st.error("❌ Incorreto. Tente novamente!")
        st.rerun()

class GenericEntityManager(SessionStateManager):
    def __init__(self, entity_name: str, fields: list):
        self.entity_name = entity_name
        self.fields = fields
        self._init_entity_session()

    def _init_entity_session(self):
        """Inicialização específica de entidades"""
        entity_key = f"{self.entity_name}_data"
        if f"entities_{entity_key}" not in st.session_state:
            st.session_state[f"entities_{entity_key}"] = {}

    def _set_ui_config(self):
        """Configuração de UI dinâmica"""
        css = f"""
        <style>
            .{self.entity_name}-card {{
                border: 2px solid {self.options.get('color', '#2ecc71')};
                border-radius: 10px;
                padding: 1rem;
                margin: 1rem 0;
            }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)

    def display_entities(self):
        """Exibe entidades com acesso seguro aos dados"""
        try:
            entity_key = f"{self.entity_name}_data"
            entities = st.session_state.entities.get(entity_key, {})
            
            st.header(f"{self.options.get('icon', '📋')} {self.entity_name.capitalize()}s Cadastrados")
            
            if not entities:
                st.info(f"Nenhum {self.entity_name} cadastrado ainda.")
                return
                
            for entity_id, entity in entities.items():
                self._render_entity(entity_id, entity)
                
        except KeyError as e:
            st.error(f"Erro de acesso aos dados: {str(e)}")
            self._init_session_state()
            st.rerun()

    def _save_entry(self, entry: Dict):
        """Salva entrada na estrutura correta do session state"""
        entity_key = f"{self.entity_name}_data"
        entity_id = f"{self.entity_name[:3]}_{uuid4().hex[:6]}"
        
        entry_data = {
            **entry,
            'id': entity_id,
            'ativo': True
        }
        
        if self.options.get('rating'):
            entry_data['classificacao'] = entry.get('classificacao', 3)
            
        # Acesso correto via estrutura hierárquica
        st.session_state.entities[entity_key][entity_id] = entry_data
        st.success(f"✅ {self.entity_name.capitalize()} salvo com sucesso!")

    def _toggle_status(self, entity_id: str):
        """Alterna status usando estrutura correta"""
        entity_key = f"{self.entity_name}_data"
        if entity_id in st.session_state.entities[entity_key]:
            current_state = st.session_state.entities[entity_key][entity_id]['ativo']
            st.session_state.entities[entity_key][entity_id]['ativo'] = not current_state
            st.rerun()

    def _delete_entity(self, entity_id: str):
        """Remove entidade da estrutura correta"""
        entity_key = f"{self.entity_name}_data"
        if entity_id in st.session_state.entities[entity_key]:
            del st.session_state.entities[entity_key][entity_id]
            st.rerun()

    def _render_entity_details(self, entity_id: str, entity: Dict):
        """Renderiza detalhes com acesso seguro"""
        entity_key = f"{self.entity_name}_data"
        cols = st.columns([3, 1, 1, 1])
        
        with cols[0]:
            for field in self.fields:
                st.markdown(f"**{field['name'].capitalize()}:** {entity.get(field['name'], 'N/A')}")
                
            if self.options.get('rating'):
                st.markdown(f"⭐ {'★' * entity.get('classificacao', 3)}")

        with cols[1]:
            if st.button("✏️ Editar", key=f"edit_{entity_id}"):
                self._edit_entity(entity_id)

        with cols[2]:
            status = "✅ Ativo" if entity['ativo'] else "⛔ Inativo"
            if st.button(status, key=f"status_{entity_id}"):
                self._toggle_status(entity_id)

        with cols[3]:
            if st.button("🗑️ Excluir", key=f"del_{entity_id}"):
                self._delete_entity(entity_id)

    def _toggle_status(self, entity_id: str):
        """Alterna status quântico da entidade"""
        entities = st.session_state[f"{self.entity_name}_data"]
        entities[entity_id]['ativo'] = not entities[entity_id]['ativo']
        st.rerun()

    def _delete_entity(self, entity_id: str):
        """Exclusão com confirmação quântica"""
        if entity_id in st.session_state[f"{self.entity_name}_data"]:
            del st.session_state[f"{self.entity_name}_data"][entity_id]
            st.rerun()

    def _get_status_icon(self, entity: Dict) -> str:
        """Retorna ícone de status personalizado"""
        if entity['ativo']:
            return self.options.get('active_icon', '🌍')
        return self.options.get('inactive_icon', '❌')

    def _edit_entity(self, entity_id: str):
        """Edição quântica da entidade (implementar)"""
        st.session_state.editing_entity = entity_id
        # Lógica de edição pode ser implementada aqui
        
    def entity_form(self):
        """Formulário quântico para criação de entidades"""
        with st.form(key=f"form_{self.entity_name}_{uuid4()}", clear_on_submit=True):
            st.subheader(f"{self.options.get('icon', '📝')} Novo {self.entity_name.capitalize()}")
            
            entry = {}
            for field in self.fields:
                self._render_form_field(field, entry)
            
            if st.form_submit_button(f"⚡ Criar {self.entity_name}"):
                self._save_entity(entry)
                st.rerun()

    def _render_form_field(self, field: dict, entry: dict):
        """Renderiza campos do formulário dinamicamente"""
        field_type = field.get('type', 'text')
        field_key = f"{field['name']}_{uuid4()}"
        
        if field_type == 'text':
            entry[field['name']] = st.text_input(
                label=field.get('label', field['name'].title()),
                key=field_key,
                help=field.get('help', '')
            )
            
        elif field_type == 'select':
            entry[field['name']] = st.selectbox(
                label=field.get('label', field['name'].title()),
                options=field.get('options', []),
                key=field_key
            )
            
        elif field_type == 'slider':
            entry[field['name']] = st.slider(
                label=field.get('label', field['name'].title()),
                min_value=field.get('min', 1),
                max_value=field.get('max', 5),
                key=field_key
            )

    def _save_entity(self, data: dict):
        """Salva entidade com validação quântica"""
        if not self._validate_entity_data(data):
            return
            
        entity_id = f"{self.entity_name[:3]}_{uuid4().hex[:6]}"
        st.session_state.entities[f"{self.entity_name}_data"][entity_id] = {
            **data,
            'id': entity_id,
            'ativo': True
        }
        st.toast(f"✅ {self.entity_name.capitalize()} criado com sucesso!", icon="⚡")

    def _validate_entity_data(self, data: dict) -> bool:
        """Validação quântica dos dados"""
        required_fields = [f['name'] for f in self.fields if f.get('required')]
        
        for field in required_fields:
            if not data.get(field):
                st.error(f"Campo obrigatório: {field}")
                return False
                
        return True
    
def exibir_laboratorio():
    """Interface principal do laboratório com funcionalidades completas"""
    st.title("🧪 Laboratório Quântico 5.0")
    
    tab1, tab2, tab3 = st.tabs(["Circuitos", "Experimentos", "Análise"])
    
    with tab1:
        col1, col2 = st.columns([1, 2])
        with col1:
            with st.container(border=True):
                st.header("Portas Quânticas")
                if st.button("H ⊗", help="Porta Hadamard"):
                    st.session_state.circuito.h(0)
                if st.button("X ⊗", help="Porta Pauli-X"):
                    st.session_state.circuito.x(0)
                if st.button("CX ⊕", help="Porta CNOT"):
                    st.session_state.circuito.cx(0, 1)
                    
        with col2:
            with st.container(border=True):
                st.header("Visualização do Circuito")
                st.write(st.session_state.circuito.draw(output='text'))
    
    with tab2:
        with st.container(border=True):
            st.header("Configuração do Experimento")
            col1, col2 = st.columns(2)
            with col1:
                st.session_state.shots = st.slider("Número de shots", 100, 5000, 1024)
            with col2:
                if st.button("⚡ Executar no Simulador", type="primary"):
                    executar_experimento(st.session_state.shots)
    
    with tab3:
        from modules.chat import QuantumEnvironmentValidator
        validator = QuantumEnvironmentValidator()
        validator.executar_verificacao()
        
        with st.expander("📊 Métricas do Sistema"):
            st.json(validator._system_diagnostic())
            
def executar_experimento(shots: int):
    """Execução completa com tratamento quântico"""
    from modules.chat import QuantumErrorHandler
    
    handler = QuantumErrorHandler()
    
    try:
        with st.status("🌀 Iniciando Simulação Quântica...") as status:
            # Configuração avançada
            simulator = AerSimulator()
            transpiled_circuit = transpile(
                st.session_state.circuito,
                simulator,
                optimization_level=3
            )
            
            # Execução com monitoramento
            job = simulator.run(transpiled_circuit, shots=shots)
            result = job.result()
            counts = result.get_counts(transpiled_circuit)
            
            # Análise dos resultados
            status.update(label="Simulação Completa!", state="complete")
            exibir_resultados_quanticos(counts)
            
    except Exception as e:
        handler._display_error_details(e, 0, str(st.session_state.circuito))
        st.error("Erro na execução quântica")

def exibir_resultados_quanticos(counts: dict):
    """Exibição avançada de resultados quânticos"""
    from modules.chat import QuantumCreativityEngine
    
    with st.container(border=True):
        st.header("📊 Resultados da Simulação")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            fig = plt.figure(figsize=(10, 6))
            plot_histogram(counts, fig=fig)
            st.pyplot(fig)
            
        with col2:
            st.subheader("Análise Quântica")
            st.write(f"Estados possíveis: {len(counts)}")
            st.write(f"Entropia: {calculate_entropy(counts):.2f} bits")
            
            if len(counts) > 1:
                st.success("✅ Efeito quântico detectado!")
            else:
                st.warning("⚠️ Comportamento clássico observado")

def mostrar_ajuda():
    """Sistema de ajuda integrado com o QuantumAssistantPro"""
    from modules.chat import QuantumAssistantPro
    
    help_text = """
    **📚 Comandos Quânticos Avançados**
    
    ```bash
    # Criação de Projetos
    !projeto criar --nome MeuProjeto
    !projeto iniciar --tipo quantico
    
    # Gerenciamento Quântico
    !circuito adicionar --porta H --qubit 0
    !circuito otimizar --nivel 3
    !executar --shots 5000
    
    # Análise e Depuração
    !diagnostico completo
    !erro analisar --recente
    !validar ambiente
    
    # Aprendizado Quântico
    !quiz iniciar
    !missao listar
    !tutorial entrelacamento
    ```
    
    **📦 Comandos de Sistema**
    ```bash
    /ambiente ativar
    /dependencias atualizar
    /validar hardware
    ```
    """
    
    with st.chat_message("assistant", avatar="🦾"):
        st.markdown(help_text)
        st.button("🧠 Mostrar Exemplos Práticos", 
                on_click=lambda: st.session_state.assistant.process_command("!exemplos praticos"))
            
def exibir_assistente(assistant):
    """Exibe a interface do assistente quântico"""
    assistant._init_session()  # Garante a inicialização
    
    # Exibir histórico
    for msg in assistant.get_state('chat_history', []):
        with st.chat_message(msg['role']):
            st.write(msg['content'])
    
    # Processar nova entrada
    if user_input := st.chat_input("Como posso ajudar?"):
        # Processar comando
        response = assistant.process_command(user_input)
        
        # Atualizar histórico
        new_history = assistant.get_state('chat_history', []) + [
            {'role': 'user', 'content': user_input},
            {'role': 'assistant', 'content': response}
        ]
        assistant.update_state('chat_history', new_history)
        st.rerun()
        
class PatternRecognizer:
    def __init__(self):
        self.pattern_db = self._load_quantum_patterns()
    
    def _load_quantum_patterns(self):
        # Carrega padrões de código de universos paralelos
        return QuantumDatabase.query("code_patterns")
    
    def recognize(self, code):
        # Usa entrelaçamento quântico para reconhecimento
        return [p for p in self.pattern_db if self._quantum_match(p, code)]
    
class QuestionnaireHandler:
    def __init__(self):
        self.protocol = ProtocolManager()
        self.states = {
            'current_question': 0,
            'user_profile': {},
            'analysis_cache': {}
        }
    
    def generate_question(self):
        questions = [
            {"id": 1, "text": "Qual o objetivo principal do seu código?", "type": "open"},
            {"id": 2, "text": "Qual nível de otimização deseja?", "type": "scale(1-5)"},
            {"id": 3, "text": "Áreas críticas para preservação:", "type": "multi-select"}
        ]
        return self._apply_protocol(questions[self.states['current_question']])
    
    def process_answer(self, answer):
        self._update_profile(answer)
        self._adaptive_analysis()
        return self._next_step()

    def _adaptive_analysis(self):
        # Análise que se adapta às respostas do usuário
        if self.states['current_question'] == 2:
            self.states['analysis_cache'] = QuantumCodeScanner(code).parallel_analysis()
            
    def quantum_priority_analysis(code):
        # Implementação realista usando Qiskit
        from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
        qr = QuantumRegister(3)
        cr = ClassicalRegister(3)
        qc = QuantumCircuit(qr, cr)
    
        # Circuito de priorização
        qc.h(qr)
        qc.cx(qr[0], qr[1])
        qc.measure(qr, cr)
    
        # Executa no simulador
        backend = Aer.get_backend('qasm_simulator')
        job = execute(qc, backend, shots=1024)
        return self._interpret_results(job.result())
    
if __name__ == "__main__":
    import platform
    st.write(f"""
    ### 📊 Diagnóstico do Sistema
    - **Sistema Operacional:** {platform.system()} {platform.release()}
    - **Arquitetura:** {platform.architecture()[0]}
    - **Python:** {platform.python_version()}
    - **Caminho Venv:** {sys.prefix}
    """)
    
    if st.button("🔄 Verificar Atualizações"):
        subprocess.run([sys.executable, "-m", "pip", "list", "--outdated"])