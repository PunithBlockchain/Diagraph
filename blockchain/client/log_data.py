# import asyncio
# import json
# import sys
# from pathlib import Path
# from anchorpy import Idl, Provider, Wallet, Program
# from solders.pubkey import Pubkey
# from solders.keypair import Keypair
# from solana.rpc.async_api import AsyncClient

# # Program ID from your IDL
# PROGRAM_ID = "xtK5pAt3VfkkcYVjJxyoS7QVxN5za5Xj93PNCqLumtX"

# async def log_to_solana(data, program_id=PROGRAM_ID):
#     """
#     Logs data to the Solana program.

#     Args:
#         data (dict): Data to log (currently unused since IDL only has 'initialize').
#         program_id (str): The Solana program ID.
#     """
#     try:
#         # Initialize the Solana client (localnet for testing)
#         async with AsyncClient("http://127.0.0.1:8899") as client:
#             # Verify connection
#             if not await client.is_connected():
#                 raise ConnectionError("Failed to connect to Solana localnet. Is it running?")

#             # Set up wallet and provider
#             wallet = Wallet(Keypair())  # New keypair; replace with your own if needed
#             provider = Provider(client, wallet)

#             # Load the IDL file
#             idl_path = Path("/Users/punithabv/Music/DiaGraph/blockchain/program/diagraph-provenance/target/idl/diagraph_provenance.json")
#             if not idl_path.exists():
#                 raise FileNotFoundError(f"IDL file not found at {idl_path}. Run 'anchor build' to generate it.")

#             with open(idl_path, "r") as f:
#                 idl_json = f.read()  # Load as string, not dict

#             # Parse the IDL into an Idl object
#             idl = Idl.from_json(idl_json)

#             # Initialize the program
#             program = Program(idl, Pubkey.from_string(program_id), provider)

#             # Call the 'initialize' instruction
#             tx = await program.rpc["initialize"](
#                 ctx={"signers": [wallet.payer]}
#             )
#             print(f"Transaction ID: {tx}")

#     except Exception as e:
#         print(f"Error: {str(e)}")
#         raise

# if __name__ == "__main__":
#     if len(sys.argv) != 2:
#         print("Usage: python log_data.py <data_file.json>")
#         sys.exit(1)

#     data_file = sys.argv[1]
#     try:
#         with open(data_file, "r") as f:
#             data = json.load(f)

#         # Since IDL only has 'initialize' with no args, data is unused
#         asyncio.run(log_to_solana({}))
#     except FileNotFoundError:
#         print(f"Error: File {data_file} not found.")
#     except json.JSONDecodeError:
#         print(f"Error: {data_file} is not a valid JSON file.")
#     except Exception as e:
#         print(f"Error: {str(e)}")

import asyncio
import json
import sys
from pathlib import Path
from anchorpy import Idl, Provider, Wallet, Program
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solana.rpc.async_api import AsyncClient

PROGRAM_ID = "xtK5pAt3VfkkcYVjJxyoS7QVxN5za5Xj93PNCqLumtX"

async def log_to_solana(data, program_id=PROGRAM_ID):
    try:
        async with AsyncClient("http://127.0.0.1:8899") as client:
            if not await client.is_connected():
                raise ConnectionError("Failed to connect to Solana localnet. Is it running?")
            
            # Load keypair from file
            keypair_path = "/Users/punithabv/.config/solana/id.json"
            if not Path(keypair_path).exists():
                raise FileNotFoundError(f"Keypair file not found at {keypair_path}")
            with open(keypair_path, "r") as f:
                keypair_data = json.load(f)
            keypair = Keypair.from_seed(bytes(keypair_data[:32]))
            
            wallet = Wallet(keypair)
            provider = Provider(client, wallet)

            idl_path = Path("/Users/punithabv/Music/DiaGraph/blockchain/program/diagraph-provenance/target/idl/diagraph_provenance.json")
            if not idl_path.exists():
                raise FileNotFoundError(f"IDL file not found at {idl_path}. Run 'anchor build'.")
            
            with open(idl_path, "r") as f:
                idl_json = f.read()
            
            try:
                idl = Idl.from_json(idl_json)
            except Exception as e:
                raise ValueError(f"Failed to parse IDL: {str(e)}")

            program = Program(idl, Pubkey.from_string(program_id), provider)

            tx = await program.rpc["initialize"](
                ctx={"signers": [wallet.payer]}
            )
            print(f"Transaction ID: {tx}")

    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python log_data.py <data_file.json>")
        sys.exit(1)

    data_file = sys.argv[1]
    try:
        with open(data_file, "r") as f:
            data = json.load(f)
        asyncio.run(log_to_solana(data))
    except FileNotFoundError:
        print(f"Error: File {data_file} not found.")
    except json.JSONDecodeError:
        print(f"Error: {data_file} is not a valid JSON file.")
    except Exception as e:
        print(f"Error: {str(e)}")