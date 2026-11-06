import numpy as np
import matplotlib.pyplot as plt

#Initializing teh the QUBIT in base states
ket0 = np.array([[1],[0]], dtype=complex)  #|0>
ket1 = np.array([[0],[1]], dtype=complex)  #|1>
state = ket0  #Original state of the qubit

#setting up the Single QuantumGate matrices

Gate_identity = np.array([[1,0],[0,1]], dtype=complex)
Gate_PauliX = np.array([[0,1], [1,0]], dtype=complex)
Gate_Hadamard = np.sqrt(1/2)*np.array([[1,1],[1,-1]], dtype=complex)
Gate_pauliY = np.array([[0, -1j], [1j, 0]], dtype=complex)
Gate_pauliZ = np.array([[1, 0], [0, -1]], dtype=complex)
Gate_S = np.array([[1, 0], [0, 1j]], dtype=complex)
Gate_T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)

#setting up the multiple Quantumgate matrices

class qubitState:
    def __init__(self, alpha=1+0j, beta=0+0j):
        self.set(alpha, beta)

    def set(self, alpha, beta):
        self._stateVector = np.array([[alpha], [beta]], dtype=complex)

    @property
    def alpha(self):
        return self._stateVector[0]

    @property
    def beta(self):
        return self._stateVector[1]

    def vector(self):
        return self._stateVector.copy()

    def probabilities(self):
        return np.abs(self._stateVector) ** 2

    def apply(self, gate):
        self._stateVector = gate@self._stateVector

class qubitRegister:
    def __init__(self):
        self.qubits = []

    def append(self, qubit):
        self.qubits.append(qubit)

        
    def __len__(self):
        return len(self.qubits)

    def __getitem__(self, i):
        return self.qubits[i]

class qubit:
    register = qubitRegister()

    def __init__(self, alpha=1+0j, beta=0+0j):
        self.state = qubitState(alpha, beta)
        qubit.register.append(self)           

    def probabilities(self):
       return self.state.probabilities()

    def apply(self, gate):
        self.state.apply(gate)


singleGates = {
    "1": ("Identity",  Gate_identity),
    "2": ("Pauli X",   Gate_PauliX),
    "3": ("Pauli Y",  Gate_pauliY),
    "4": ("Pauli Z",  Gate_pauliZ),
    "5": ("Hadamard",  Gate_Hadamard),
    "6": ("S",  Gate_S),
    "7": ("T",  Gate_T),
}

    #gate that applies a given function
def applyGate(gate, stateParameter):
    return gate@stateParameter

def kroneckerProduct():
    resultant=qubit.register[0].state.vector()
    for i in range(1, len(qubit.register)):
        resultant=np.kron(resultant, qubit.register[i].state.vector())
    return resultant

#main program

while True:
    menu = input('''
    1. Create a qubit
    2. Apply gate to singular qubit
    3. Combine the qubits
    q. Quit
    Choose: ''')
    print("")

    if menu == "q":
        break

    match menu:
        case "1":
            initializationChoice = input('''
            1. |0>
            2. |1>
            3. Custom
            Initialize the qubit: ''')
            print("")
            
            if initializationChoice == "1":
                q = qubit(1, 0)
            elif initializationChoice == "2":
                q = qubit(0, 1)
            elif initializationChoice == "3":
                alpha = complex(input("Enter the coefficient of |0> : "))
                beta = complex(input("Enter the coefficient of |1> : "))
                if not np.isclose(np.abs(alpha)**2 + np.abs(beta)**2, 1):
                    print("Invalid: probabilities must add up to 1")
                    continue
                q = qubit(alpha, beta)
            else:
                print("Invalid choice")
                continue
            print(f"Created qubit #{len(qubit.register)}")
            print(f"  State:         {np.round(q.state.vector().flatten(), 3)}")
            print(f"  Probabilities: {np.round(q.probabilities().flatten(), 3)}")
        case "2":
            if(len(qubit.register)==0):
                print("No qubit created")
                continue
            for i in range(0, len(qubit.register)):
                print(f"qubit no.{i+1}")
            qubitChoice = int(input("Enter which qubit: "))
            print("")
            target = qubit.register[qubitChoice-1]
            print("\nGates:")
            for key, (name, _) in singleGates.items():
                print(f"  {key}. {name}")
            choice = input("Choose a gate (or q to quit): ")
        
            if choice == "q":
                break
            if choice not in singleGates:
                print("Invalid entry")
                continue
            
            name, gate = singleGates[choice]
            target.apply(gate)
            print("")
            print(f"After {name}:")
            print(f"  State:         {np.round(target.state.vector().flatten(), 3)}")
            print(f"  Probabilities: {np.round(target.probabilities().flatten(), 3)}")
        case "3":
            if(len(qubit.register)<2):
                print("Not enough qubits")
                continue
            result = kroneckerProduct()
            n = len(qubit.register)
            print(f"Combined state of {n} qubits ({2**n} amplitudes):")
            for i, amp in enumerate(result):
                label = format(i, f"0{n}b")      # 0 -> '00', 1 -> '01', ...
                print(f"  |{label}>  amplitude {np.round(amp, 3)}   probability {np.round(abs(amp)**2, 3)}")
        case _:
            print("Invalid input")
            continue
                