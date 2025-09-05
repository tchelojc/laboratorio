from qiskit import QuantumCircuit, transpile, Aer, execute

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])  # Medição clássica
qc.x(0).c_if(0, 1)          # Porta X condicional ao resultado clássico
qc.measure_all()

# Execute no simulador ou hardware IBM
simulator = Aer.get_backend('qasm_simulator')
job = execute(qc, simulator, shots=1000)
result = job.result()
counts = result.get_counts(qc)
print(counts)