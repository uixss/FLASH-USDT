import customtkinter as ctk
from tkinter import messagebox
from web3 import Web3
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root = ctk.CTk()
window_width = 950
window_height = 500
root.geometry(f"{window_width}x{window_height}")
root.title("𝐒𝐇𝐈𝐓 𝐔𝐍𝐃𝐄𝐑 💀")
root.configure(bg="#262626")
root.resizable(False, False)
root.overrideredirect(True)
root.wm_attributes('-alpha', 0.92)
root.grid_columnconfigure(0, weight=3)
root.grid_columnconfigure(1, weight=1)

# Movimiento de la ventana
root.x = None
root.y = None

def start_move(event):
    root.x = event.x
    root.y = event.y

def stop_move(event):
    root.x = None
    root.y = None

def on_motion(event):
    if root.x is not None and root.y is not None:
        deltax = event.x - root.x
        deltay = event.y - root.y
        x = root.winfo_x() + deltax
        y = root.winfo_y() + deltay
        root.geometry(f"+{x}+{y}")

root.bind("<Button-1>", start_move)
root.bind("<B1-Motion>", on_motion)
root.bind("<ButtonRelease-1>", stop_move)

# Web3 Initialization
infura_url = "https://mainnet.infura.io/v3/ID"
web3 = Web3(Web3.HTTPProvider(infura_url))

cryptocurrencies = {
    "USDT": {"address": "0xdAC17F958D2ee523a2206206994597C13D831ec7", "decimals": 6},
    "WBTC": {"address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599", "decimals": 8},
    "USDC": {"address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606EB48", "decimals": 6},
    "DAI": {"address": "0x6B175474E89094C44Da98b954EedeAC495271d0F", "decimals": 18},
    "PEPE": {"address": "0x6982508145454Ce325dDbE47a25d4ec3d2311933", "decimals": 18},
    "FTM": {"address": "0x4e15361FD6b4BB609Fa63c81A2be19d873717870", "decimals": 18},
    "SHIB": {"address": "0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE", "decimals": 18},
    "MATIC": {"address": "0x7D1Afa7B718fb893dB30A3aBc0Cfc608AaCfeBB0", "decimals": 18},
    "UNI": {"address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984", "decimals": 18},
    "TON": {"address": "0x2ee543c7a6D02aC3D1E5aA0e6A7bD71cB1e4F830", "decimals": 9}
}

last_transaction = None

# Funciones
def validate_and_convert_address(address):
    if not web3.is_address(address):
        raise ValueError("Invalid Ethereum address.")
    return web3.to_checksum_address(address)

def send_transaction():
    global last_transaction
    private_key = private_key_entry.get()
    delivery_address = delivery_address_entry.get()
    send_amount = amount_entry.get()
    selected_currency = currency_combobox.get()

    try:
        delivery_address = validate_and_convert_address(delivery_address)
        currency_data = cryptocurrencies[selected_currency]
        contract_address = currency_data["address"]
        decimals = currency_data["decimals"]
        send_amount = int(float(send_amount) * (10 ** decimals))
        account = web3.eth.account.from_key(private_key)
        sender_address = account.address
        method_id = "0xa9059cbb"
        padded_address = delivery_address[2:].zfill(64)
        padded_amount = hex(send_amount)[2:].zfill(64)
        data = method_id + padded_address + padded_amount
        nonce = web3.eth.get_transaction_count(sender_address)
        gas_price = web3.to_wei(3, "gwei")
        gas_limit = 60000

        transaction = {
            "to": contract_address,
            "value": 0,
            "gas": gas_limit,
            "gasPrice": gas_price,
            "nonce": nonce,
            "data": data,
            "chainId": 1,
        }

        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

        tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
        tx_hash_hex = web3.to_hex(tx_hash)

        last_transaction = {
            "nonce": nonce,
            "gasPrice": gas_price,
            "private_key": private_key
        }

        root.clipboard_clear()
        root.clipboard_append(tx_hash_hex)
        root.update()

        messagebox.showinfo("Success", f"Transaction sent!\nHash: {tx_hash_hex}\n(TxID copied to clipboard)")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to send transaction:\n{str(e)}")

# Componentes de la interfaz
private_key_entry = ctk.CTkEntry(root, placeholder_text="Private Key", width=400, show="*")
private_key_entry.grid(row=0, column=0, padx=20, pady=10)

delivery_address_entry = ctk.CTkEntry(root, placeholder_text="Delivery Address", width=400)
delivery_address_entry.grid(row=1, column=0, padx=20, pady=10)

amount_entry = ctk.CTkEntry(root, placeholder_text="Amount", width=400)
amount_entry.grid(row=2, column=0, padx=20, pady=10)

currency_combobox = ctk.CTkComboBox(root, values=list(cryptocurrencies.keys()))
currency_combobox.grid(row=3, column=0, padx=20, pady=10)
currency_combobox.set("USDT")

send_button = ctk.CTkButton(root, text="Send Transaction", command=send_transaction)
send_button.grid(row=4, column=0, padx=20, pady=20)

root.mainloop()
