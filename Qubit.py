import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
import textwrap


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
Gate_Sdg = np.array([[1, 0], [0, -1j]], dtype=complex)
Gate_Tdg = np.array([[1, 0], [0, np.exp(-1j * np.pi / 4)]], dtype=complex)


#setting up the 2 qubit quantumgate matrices
Gate_CNOT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
Gate_CNOT01 = np.array([[1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]], dtype=complex)
Gate_2Identity = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=complex)
Gate_CpauliX = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)
Gate_CpauliY = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, -1j], [0, 0, 1j, 0]], dtype=complex)
Gate_CpauliZ = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]], dtype=complex)
Gate_CHadamard = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, np.sqrt(1/2), np.sqrt(1/2)], [0, 0, np.sqrt(1/2), -np.sqrt(1/2)]], dtype=complex)
Gate_CS = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1j]], dtype=complex)
Gate_CT = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, np.exp(1j * np.pi / 4)]], dtype=complex)
Gate_SWAP = np.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex)
Gate_CSdg = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1j]], dtype=complex)
Gate_CTdg = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, np.exp(-1j * np.pi / 4)]], dtype=complex)

h = np.sqrt(1/2)

#setting up the 3 qubit quantumgate matrices
Gate_3Identity = np.eye(8, dtype=complex)
Gate_Toffoli = np.array([
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1, 0]], dtype=complex)
Gate_CCpauliY = np.array([
    [1, 0, 0, 0, 0, 0, 0,   0],
    [0, 1, 0, 0, 0, 0, 0,   0],
    [0, 0, 1, 0, 0, 0, 0,   0],
    [0, 0, 0, 1, 0, 0, 0,   0],
    [0, 0, 0, 0, 1, 0, 0,   0],
    [0, 0, 0, 0, 0, 1, 0,   0],
    [0, 0, 0, 0, 0, 0, 0,  -1j],
    [0, 0, 0, 0, 0, 0, 1j,  0]], dtype=complex) 
Gate_CCZ = np.diag([1, 1, 1, 1, 1, 1, 1, -1]).astype(complex)
Gate_CCHadamard = np.array([
    [1, 0, 0, 0, 0, 0, 0,  0],
    [0, 1, 0, 0, 0, 0, 0,  0],
    [0, 0, 1, 0, 0, 0, 0,  0],
    [0, 0, 0, 1, 0, 0, 0,  0],
    [0, 0, 0, 0, 1, 0, 0,  0],
    [0, 0, 0, 0, 0, 1, 0,  0],
    [0, 0, 0, 0, 0, 0, h,  h],
    [0, 0, 0, 0, 0, 0, h, -h]], dtype=complex)
Gate_CCS = np.array([
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1j]], dtype=complex)
Gate_CCSdg = np.array([
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, -1j]], dtype=complex)
Gate_CCT = np.array([
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, np.exp(1j * np.pi / 4)]], dtype=complex)
Gate_CCTdg = np.array([
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, np.exp(-1j * np.pi / 4)]], dtype=complex)
Gate_CSWAP = np.array([
    [1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1]], dtype=complex)

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
    "3": ("Controlled Identity",  Gate_2Identity),
    "4": ("Controlled Pauli-X",  Gate_CpauliX),
    "5": ("Controlled Pauli-Y",  Gate_CpauliY),
    "6": ("Controlled Pauli-Z",  Gate_CpauliZ),
    "7": ("Controlled Hadamard",  Gate_CHadamard),
    "8": ("Controlled S",  Gate_CS),
    "9": ("Controlled T",  Gate_CT),
    "10": ("SWAP",  Gate_SWAP),
    "11": ("Controlled S-dagger",  Gate_CSdg),
    "12": ("Controlled T-dagger",  Gate_CTdg),
}

#Holding the dictionary for multi qubit gates
threeGates = {
    "1": ("Identity",  Gate_3Identity),
    "2": ("Toffoli",  Gate_Toffoli),
    "3": ("Controlled C Pauli-Y",  Gate_CCpauliY),
    "4": ("Controlled C Pauli-Z",  Gate_CCZ),
    "5": ("Controlled C Hadamard",  Gate_CCHadamard),
    "6": ("Controlled C S",  Gate_CCS),
    "7": ("Controlled C S dagger",  Gate_CCSdg),
    "8": ("Controlled C T",  Gate_CCT),
    "9": ("Controlled C T dagger",  Gate_CCTdg),
    "10": ("Controlled SWAP",  Gate_CSWAP),
}

#Holding the dictionary for single qubit gates
singleGates = {
    "1": ("Identity",  Gate_identity),
    "2": ("Pauli-X",   Gate_PauliX),
    "3": ("Pauli-Y",  Gate_pauliY),
    "4": ("Pauli-Z",  Gate_pauliZ),
    "5": ("Hadamard",  Gate_Hadamard),
    "6": ("S",  Gate_S),
    "7": ("T",  Gate_T),
    "8": ("S dagger", Gate_Sdg),
    "9": ("T dagger", Gate_Tdg),
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

    # Palette
    BG = "#14141A"            # background (almost black)
    MAJORELLE = "#6050DC"     # sphere surface
    ARROW = "#8F8FFF"         # state arrow and dot (brighter so it pops on dark)
    GRID = "#D6D6FF"          # wireframe and equator (light periwinkle)
    LIGHT = "#E8E8FF"         # axes, labels, title

    # Background
    ax.figure.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    # Sphere surface and wireframe
    u = np.linspace(0, 2 * np.pi, 40)
    v = np.linspace(0, np.pi, 20)
    xs = np.outer(np.cos(u), np.sin(v))
    ys = np.outer(np.sin(u), np.sin(v))
    zs = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_surface(xs, ys, zs, color=MAJORELLE, alpha=0.15, linewidth=0)
    ax.plot_wireframe(xs, ys, zs, color=GRID, alpha=0.35, linewidth=0.4)

    # Equator
    t = np.linspace(0, 2 * np.pi, 100)
    ax.plot(np.cos(t), np.sin(t), 0 * t, color=GRID, lw=1.2, alpha=0.9)

    # Coordinate axes
    ax.plot([-1.2, 1.2], [0, 0], [0, 0], color=LIGHT, lw=0.8)
    ax.plot([0, 0], [-1.2, 1.2], [0, 0], color=LIGHT, lw=0.8)
    ax.plot([0, 0], [0, 0], [-1.2, 1.2], color=LIGHT, lw=0.8)

    # Labels
    ax.text(0, 0, 1.3, "|0>", ha="center", fontsize=12, color=LIGHT)
    ax.text(0, 0, -1.4, "|1>", ha="center", fontsize=12, color=LIGHT)
    ax.text(1.35, 0, 0, "+x", ha="center", color=LIGHT)
    ax.text(0, 1.35, 0, "+y", ha="center", color=LIGHT)

    # The qubit's state as an arrow
    x, y, z = blochVector(stateParameter)
    ax.quiver(0, 0, 0, x, y, z, color=ARROW, linewidth=3, arrow_length_ratio=0.15)
    ax.scatter([x], [y], [z], color=ARROW, s=40)

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_box_aspect((1, 1, 1))
    ax.set_axis_off()
    ax.set_title(f"Bloch vector for qubit #{no}: ({x:.2f}, {y:.2f}, {z:.2f})", color=LIGHT)
    plt.draw()
    plt.pause(0.1)

def draw_message(ax, message):
    BG = "#14141A"        # same background as draw_bloch
    LIGHT = "#E8E8FF"     # message text
    ACCENT = "#8F8FFF"    # title

    ax.clear()
    ax.figure.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_axis_off()

    # Wrap long text so it fits inside the window
    wrapped = "\n".join(textwrap.wrap(message, width=35))

    # text2D places text in axes coordinates (0 to 1), so it stays centred
    # even though the axes is 3D
    ax.text2D(0.5, 0.5, wrapped, transform=ax.transAxes,
              ha="center", va="center", fontsize=13,
              color=LIGHT, linespacing=1.6)
    ax.set_title("Bloch sphere unavailable", color=ACCENT)

    plt.draw()
    plt.pause(0.1)


#initializing and displaying bloch sphere
plt.ion()
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection="3d")


def showState(state, n, title):
    print(f"\n{title}")
    for i, amp in enumerate(state):
        label = format(i, f"0{n}b")
        a = amp.item()
        print(f"  |{label}>  amplitude {np.round(a, 3)}   probability {abs(a)**2:.3f}")


#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\
#MAIN PROGRAM THAT RUNS PERPETUALLY
#|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\


while True:

    print("")
    print("")
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
                continue
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
            if qubitChoice > len(qubit.register) and qubitChoice < 1:
                print("Invalid")
                continue
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
            Choose the number of qubits in the qubit system: ''')

            match choiceOfQubit:
                case "1":
                    n = 2
                    multi = multiGates
                case "2":
                    n = 3
                    multi = threeGates
                case _:
                    print("Invalid")
                    continue

            if len(qubit.register) != n:
                print("Invalid number of qubits in the register")
                continue

            result = kroneckerProduct()          # created once, updated by every gate below
            showState(result, n, f"Combined state of {n} qubits ({2**n} amplitudes):")

            while True:
                draw_message(ax, "Bloch sphere cannot be viewed during multi qubit operations "
                 "as it is only a representation for a single qubit. In higher qubit systems, the sphere is redundant. Please leave the current menu to go back and view singular, individual qubits on the sphere.")
                gateChoice = input('''
            1. Apply a single qubit gate to all qubits
            2. Apply a multi qubit gate to the qubit system
            Choose an option (or q to go back to the main menu): ''')

                if gateChoice == "q":
                    break

                match gateChoice:
                    case "1":
                        gates = singleGates
                    case "2":
                        gates = multi
                    case _:
                        print("Invalid entry")
                        continue

                print("\nGates:")
                for key, (name, _) in gates.items():
                    print(f"  {key}. {name}")
                choice = input("Choose a gate (or q to go back): ")

                if choice == "q":
                    continue
                if choice not in gates:
                    print("Invalid entry")
                    continue

                name, gate = gates[choice]
                if gateChoice == "1":
                    gate = reduce(np.kron, [gate] * n)   # same gate on every qubit

                result = gate @ result
                showState(result, n, f"After {name}:")
        #DEFAULT CASE FOR INVALID INPUT
        case _:
            print("Invalid input")
            continue
                