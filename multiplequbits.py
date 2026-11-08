import numpy as np
import matplotlib.pyplot as plt

#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\
#Initiallizing basic quantum states and matrices
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\


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


#setting up the multi quantumgate matrices
Gate_CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
Gate_CNOT01 = np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]], dtype=complex)
Gate_CIdentity = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=complex)
Gate_CpauliX = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
Gate_CpauliY = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, -1j], [0, 0, 1j, 0]], dtype=complex)
Gate_CpauliZ = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]], dtype=complex)
Gate_CHadamard = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, np.sqrt(1/2), np.sqrt(1/2)], [0, 0, np.sqrt(1/2), -np.sqrt(1/2)]], dtype=complex)
Gate_CS = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1j]], dtype=complex)
Gate_CT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -np.exp(1j * np.pi / 4)]], dtype=complex)
Gate_SWAP = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex)


#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\
#Classes that hold the qubit states, qubits and qubit register
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\


#A class that holds the vector propery of a qubit state, has alpha and beta values
class qubitState:

    #initialization of the class
    def __init__(self, alpha=1+0j, beta=0+0j):
        self.set(alpha, beta)

    #setting the qubit state
    def set(self, alpha, beta):
        self._stateVector = np.array([[alpha], [beta]], dtype=complex)

    #returns alpha value
    @property
    def alpha(self):
        return self._stateVector[0]

    #returns beta value
    @property
    def beta(self):
        return self._stateVector[1]

    #return the state vector
    def vector(self):
        return self._stateVector.copy()

    #returns the probability of that state vector
    def probabilities(self):
        return np.abs(self._stateVector) ** 2

    #Used to apply gate on that stateVector
    def apply(self, gate):
        self._stateVector = gate@self._stateVector

#qubit register: Has an array of all the created qubits with a related qubit state class to hold properties
class qubitRegister:

    #initializing the qubitregister
    def __init__(self):
        self.qubits = []

    #funciton that appends a new qubit into the register
    def append(self, qubit):
        self.qubits.append(qubit)

    #a dunder function that returns the length of the qubit register
    def __len__(self):
        return len(self.qubits)

    #a dunder function that returns a singular qubit from the register
    def __getitem__(self, i):
        return self.qubits[i]

#Class for a singular qubit
class qubit:

    #setting up the actual register
    register = qubitRegister()

    #initializing the qubit using the previous qubit state class
    def __init__(self, alpha=1+0j, beta=0+0j):
        self.state = qubitState(alpha, beta)
        qubit.register.append(self)           

    #Returns the probability of the specific qubit from the probability function previoiusly
    def probabilities(self):
       return self.state.probabilities()

    #used ti apply the gate to specific qubit
    def apply(self, gate):
        self.state.apply(gate)

#return the kronecker product of every single qubit in the register
def kroneckerProduct():
    resultant=qubit.register[0].state.vector()
    for i in range(1, len(qubit.register)):
        resultant=np.kron(resultant, qubit.register[i].state.vector())
    return resultant


#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\
#DICTIONARIES FOR THE GATES
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\


#Holding the dictionary for multi qubit gates
multiGates = {
    "1": ("CNOT",  Gate_CNOT),
    "2": ("CNOT01",   Gate_CNOT01),
    "3": ("Controlled Identity",  Gate_CIdentity),
    "4": ("Controlled PauliX",  Gate_CpauliX),
    "5": ("Controlled PauliY",  Gate_CpauliY),
    "6": ("Controlled PauliZ",  Gate_CpauliZ),
    "7": ("Controlled Hadamard",  Gate_CHadamard),
    "8": ("Controlled S",  Gate_CS),
    "9": ("Controlled T",  Gate_CT),
    "10": ("SWAP",  Gate_SWAP),
}

#Holding the dictionary for single qubit gates
singleGates = {
    "1": ("Identity",  Gate_identity),
    "2": ("Pauli X",   Gate_PauliX),
    "3": ("Pauli Y",  Gate_pauliY),
    "4": ("Pauli Z",  Gate_pauliZ),
    "5": ("Hadamard",  Gate_Hadamard),
    "6": ("S",  Gate_S),
    "7": ("T",  Gate_T),
}



#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\
#FUNCTIONS REGARDING THE DRAWING OF BLOCH SPHERE AND DISPLAYING ITS BLOCH VECTOR
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\


#getting the coordinates for the blochvector
def blochVector(stateParameter):
    # alpha = stateParameter[0][0]
    # beta = stateParameter[1][0]
    # theta = 2*(np.arccos(np.abs(alpha)))
    # phi = (np.log(beta/np.sin(theta/2)))/1j
    # x=np.sin(theta)*np.cos(phi)
    # y=np.sin(theta)*np.sin(phi)
    # z=np.cos(theta)
    # return x,y,z

    alpha = stateParameter[0][0]
    beta = stateParameter[1][0]
    theta = 2 * np.arccos(np.clip(np.abs(alpha), 0, 1))
    phi = np.angle(beta) - np.angle(alpha)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return x, y, z


#drawing the bloch sphere
def draw_bloch(ax, stateParameter, no):
    ax.clear()

    # Sphere surface and wireframe
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 20)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(xs, ys, zs, color="lightblue", alpha=0.15, linewidth=0)
    ax.plot_wireframe(xs, ys, zs, color="gray", alpha=0.2, linewidth=0.3)

    # Equator
    t = np.linspace(0, 2 * np.pi, 100)
    ax.plot(np.cos(t), np.sin(t), 0 * t, color="gray", lw=0.8)

    # Coordinate axes
    ax.plot([-1.2, 1.2], [0, 0], [0, 0], "k-", lw=0.8)
    ax.plot([0, 0], [-1.2, 1.2], [0, 0], "k-", lw=0.8)
    ax.plot([0, 0], [0, 0], [-1.2, 1.2], "k-", lw=0.8)

    # Labels
    ax.text(0, 0, 1.3, "|0>", ha="center", fontsize=12)
    ax.text(0, 0, -1.4, "|1>", ha="center", fontsize=12)
    ax.text(1.35, 0, 0, "+x", ha="center")
    ax.text(0, 1.35, 0, "+y", ha="center")

    # The qubit's state as an arrow
    x, y, z = blochVector(stateParameter)
    ax.quiver(0, 0, 0, x, y, z, color="red", linewidth=3, arrow_length_ratio=0.15)
    ax.scatter([x], [y], [z], color="red", s=40)

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_box_aspect((1, 1, 1))
    ax.set_axis_off()
    ax.set_title(f"Bloch vector for qubit #{no}: ({x:.2f}, {y:.2f}, {z:.2f})")
    plt.draw()
    plt.pause(0.1)



#initializing and displaying bloch sphere
plt.ion()
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection="3d")



#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\
#MAIN PROGRAM THAT RUNS PERPETUALLY
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\


while True:

    #MAIN MENU TO CHOSE THE PROCESS WE WANT TO CONDUCT
    menu = input('''
    1. Create a qubit
    2. Apply gate to singular qubit
    3. Display a qubit in a bloch sphere
    4. Display the Total qubit system
    5. Perform operations on the total qubit system
    q. Quit
    Choose: ''')
    print("")

    #EXIT CLAUSE FOR THE MENU
    if menu == "q":
        break

    match menu:

        #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\
        #CASE 1 CREATING AND INITIALIZING A QUBIT
        #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\
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
            draw_bloch(ax, q.state.vector(), len(qubit.register))



        #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\
        #CASE 2 FOR APPLYING GATE TO A SINGULAR QUBIT
        #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\        
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
            draw_bloch(ax, target.state.vector(), qubitChoice)
            print("")
            print(f"After {name}:")
            print(f"  State:         {np.round(target.state.vector().flatten(), 3)}")
            print(f"  Probabilities: {np.round(target.probabilities().flatten(), 3)}")



        #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\
        #DISPLAYING A SELECTED QUBIT IN THE BLOCH SPHERE
        #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\
        case "3":
            if (len(qubit.register)==0):
                print("Not enough qubits")
                continue
            for i in range(0, len(qubit.register)):
                print(f"qubit no.{i+1}")
            qubitChoice = int(input("Enter which qubit: "))
            draw_bloch(ax, qubit.register[qubitChoice-1].state.vector(), qubitChoice)



        #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\
        #DISPLAY THE TOTAL MULTI-QUBIT SYSTEM
        #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\
        case "4":
            if(len(qubit.register)<2):
                print("Not enough qubits")
                continue
            result = kroneckerProduct()
            n = len(qubit.register)
            print(f"Combined state of {n} qubits ({2**n} amplitudes):")
            for i, amp in enumerate(result):
                label = format(i, f"0{n}b")      # 0 -> '00', 1 -> '01', ...
                print(f"  |{label}>  amplitude {np.round(amp, 3)}   probability {np.round(abs(amp)**2, 3)}")


        #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\
        #PERFORMING OPERATIONS ON THE MULTI-QUBIT SYSTEM
        #|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\
        case "5":
            choiceOfQubit = input('''
            1. 2 Qubits
            2. 3 Qubits
            Choose the number of qubits in the qubit system:''')
            match choiceOfQubit:
                case "1":
                    if len(qubit.register)!=2:
                        print("Invalid number of qubits in the register")
                        continue
                    result = kroneckerProduct()
                    n = len(qubit.register)
                    print(f"Combined state of {n} qubits ({2**n} amplitudes):")
                    for i, amp in enumerate(result):
                        label = format(i, f"0{n}b")      # 0 -> '00', 1 -> '01', ...
                        print(f"  |{label}>  amplitude {np.round(amp, 3)}   probability {np.round(abs(amp)**2, 3)}")
                    print("\nGates:")
                    for key, (name, _) in multiGates.items():
                        print(f"  {key}. {name}")
                    choice = input("Choose a gate (or q to quit): ")
                
                    if choice == "q":
                        continue
                    if choice not in multiGates:
                        print("Invalid entry")
                        continue

                    name, gate = multiGates[choice]
                    result=gate@result
                    print("")
                    print(f"After {name}:")
                    for i, amp in enumerate(result):
                        label = format(i, f"0{n}b")      # 0 -> '00', 1 -> '01', ...
                        print(f"  |{label}>  amplitude {np.round(amp, 3)}   probability {np.round(abs(amp)**2, 3)}")
                case "2":
                    if len(qubit.register)!=3:
                        print("Invalid number of qubits in the register")
                        continue
                    print("in the works...")
                case _:
                    print("Invalid")
                    continue
        #DEFAULT CASE FOR INVALID INPUT
        case _:
            print("Invalid input")
            continue
                