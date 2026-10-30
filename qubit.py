import numpy as np
import matplotlib.pyplot as plt

#Initializing teh the QUBIT in base states
ket0 = np.array([[1],[0]], dtype=complex)  #|0>
ket1 = np.array([[0],[1]], dtype=complex)  #|1>
state = ket0  #Original state of the qubit

#setting up the QuantumGate matrices

Gate_identity = np.array([[1,0],[0,1]], dtype=complex)
Gate_PauliX = np.array([[0,1], [1,0]], dtype=complex)
Gate_Hadamard = np.sqrt(1/2)*np.array([[1,1],[1,-1]], dtype=complex)
Gate_pauliY = np.array([[0, -1j], [1j, 0]], dtype=complex)
Gate_pauliZ = np.array([[1, 0], [0, -1]], dtype=complex)
Gate_S = np.array([[1, 0], [0, 1j]], dtype=complex)
Gate_T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]], dtype=complex)

gates = {
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

#gate that returns the probabilities each qubit ket
def probability(stateParameter):
    return np.abs(stateParameter) ** 2

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



#taking user input
initializationChoice = int(input('''1. |0>
2. |1>
3. Custom
Initialize the qubit: '''))

match initializationChoice:
    case 1:
        state = ket0
    case 2:
        state = ket1
    case 3:
        alpha = complex(input("Enter the coeffecients of |0> : "))
        beta = complex(input("Enter the coeffecients of |1> : "))
        if (np.square(np.abs(alpha)) + np.square(np.abs(beta)) != 1):
            print("Invalid")
            exit()
            state = np.array([[alpha], [beta]], dtype=complex)
    case _:
        print("Invalid choice")
        exit()

#drawing the bloch sphere
def draw_bloch(ax, stateParameter):
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
    ax.set_title(f"Bloch vector: ({x:.2f}, {y:.2f}, {z:.2f})")
    plt.draw()
    plt.pause(0.1)


#initializing and displaying bloch sphere
plt.ion()
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection="3d")
draw_bloch(ax, state)

#main program

while True:
    print("\nGates:")
    for key, (name, _) in gates.items():
        print(f"  {key}. {name}")
    choice = input("Choose a gate (or q to quit): ")

    if choice == "q":
        break
    if choice not in gates:
        print("Invalid entry")
        continue

    name, gate = gates[choice]
    state = applyGate(gate, state)
    print(f"After {name}:")
    print(f"  State:        {np.round(state.flatten(), 3)}")
    print(f"  Probabilities:    {np.round(probability(state), 3)}")
    draw_bloch(ax, state)
    