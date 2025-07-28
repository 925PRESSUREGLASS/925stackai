


import streamlit as st
import os
import sys
from pathlib import Path

# --- Simplified import for utils.kb_loader ---
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from utils.kb_loader import load_kb, search_kb

# Ensure project root is in sys.path for imports
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from agents.quote_agent import run_quote
from gui.components import parse_quote_output, render_quote


def main() -> None:

    st.set_page_config(page_title="Quote Assistant", layout="wide")
    st.title("Quoting Assistant")

    # --- Load Knowledge Base (KB) at startup ---
    if "kb" not in st.session_state:
        st.session_state.kb = load_kb("925stackai-KB")

    if "history" not in st.session_state:
        st.session_state.history = []

    from pathlib import Path

    import GPUtil
    import psutil
    from langchain_community.vectorstores import FAISS


    left, right = st.columns(2)

    # --- Interactive Quote Calculator ---
    with st.sidebar:
        st.header("Quick Quote Calculator")
        # Load pricing config
        import json
        config_path = Path(__file__).parent.parent / "configs" / "pricing.json"
        with open(config_path, "r", encoding="utf-8") as f:
            pricing_config = json.load(f)

        service_options = [k for k in pricing_config.keys() if k != "surcharge"]
        service = st.selectbox("Service Type", service_options, key="service_type")
        qty = st.number_input("Quantity", min_value=1, value=1, step=1, key="qty")
        # Dynamically get available sizes from config
        size_options = ["standard", "large"]
        size_options += [k for k in pricing_config.keys() if k in ["small", "medium", "extra_large"]]
        size = st.selectbox("Size", size_options, key="size")
        storey = st.selectbox("Storey", [1, 2, 3], key="storey")
        # Surcharge options
        surcharge_keys = list(pricing_config.get("surcharge", {}).keys())
        selected_surcharges = st.multiselect("Surcharges", surcharge_keys, key="surcharges")
        # Suburb selector for travel surcharge
        suburb_options = [
            "None", "Cottesloe", "Subiaco", "Fremantle", "Claremont", "Mosman Park",
            "Peppermint Grove", "Nedlands", "Dalkeith", "Crawley", "Shenton Park"
        ]
        suburb = st.selectbox("Suburb", suburb_options, key="suburb")
        suburb_map = {
            "Cottesloe": "travel_cottesloe",
            "Subiaco": "travel_subiaco",
            "Fremantle": "travel_fremantle",
            "Claremont": "travel_claremont",
            "Mosman Park": "travel_mosman_park",
            "Peppermint Grove": "travel_peppermint_grove",
            "Nedlands": "travel_nedlands",
            "Dalkeith": "travel_dalkeith",
            "Crawley": "travel_crawley",
            "Shenton Park": "travel_shenton_park"
        }
        if suburb != "None":
            surcharge_key = suburb_map.get(suburb)
            if surcharge_key and surcharge_key not in selected_surcharges:
                selected_surcharges.append(surcharge_key)

        # Multi-window quote support
        if "quote_items" not in st.session_state:
            st.session_state["quote_items"] = []

        if st.button("Add Item", key="add_item_btn"):
            st.session_state["quote_items"].append({
                "service": service,
                "qty": qty,
                "size": size
            })


        st.markdown("### Quote Items")
        if st.session_state["quote_items"]:
            remove_idx = st.number_input("Remove Item #", min_value=1, max_value=len(st.session_state["quote_items"]), value=1, step=1, key="remove_item_idx")
            edit_idx = st.number_input("Edit Item #", min_value=1, max_value=len(st.session_state["quote_items"]), value=1, step=1, key="edit_item_idx")
            for idx, item in enumerate(st.session_state["quote_items"]):
                st.write(f"{idx+1}. {item['service']} ({item['size']}) x {item['qty']}")
            if st.button("Remove Selected Item", key="remove_item_btn"):
                if 1 <= remove_idx <= len(st.session_state["quote_items"]):
                    st.session_state["quote_items"].pop(remove_idx-1)
            if st.button("Edit Selected Item", key="edit_item_btn"):
                if 1 <= edit_idx <= len(st.session_state["quote_items"]):
                    item = st.session_state["quote_items"][edit_idx-1]
                    new_service = st.selectbox("Edit Service Type", service_options, index=service_options.index(item["service"]), key="edit_service")
                    new_qty = st.number_input("Edit Quantity", min_value=1, value=item["qty"], step=1, key="edit_qty")
                    new_size = st.selectbox("Edit Size", size_options, index=size_options.index(item["size"]), key="edit_size")
                    if st.button("Save Item Changes", key="save_edit_btn"):
                        st.session_state["quote_items"][edit_idx-1] = {
                            "service": new_service,
                            "qty": new_qty,
                            "size": new_size
                        }
        else:
            st.info("No quote items added yet.")

        if st.button("Calculate Total Quote", key="calc_total_quote_btn"):
            # Aggregate all items into a single scope
            total_items = []
            total = 0.0
            all_surcharges = {k: True for k in selected_surcharges}
            for item in st.session_state["quote_items"]:
                scope = {
                    "service": item["service"],
                    "qty": item["qty"],
                    "size": item["size"],
                    "storey": storey,
                    "surcharges": all_surcharges
                }
                from logic.pricing_rules import calculate_price
                result = calculate_price(scope)
                total_items.extend(result["items"])
                total += result["total"]
            st.markdown(f"### Total Quote Result")
            for item in total_items:
                unit_price = item["unit_price"]
                size_val = item["size"]
                subtotal = item["subtotal"]
                st.write(f"Service: {item['service']}")
                st.write(f"Unit Price: {unit_price}")
                st.write(f"Size: {size_val}")
                st.write(f"Quantity: {item['qty']}")
                st.write(f"Subtotal: ${subtotal}")
            st.write(f"Surcharges: {all_surcharges}")
            st.write(f"Total: ${round(total,2)}")

            # --- Save quick quote and grading to vector store ---
            # Compose a prompt summary for the quick quote
            prompt_summary = "Quick Quote: " + ", ".join([
                f"{item['qty']}x {item['service']} ({item['size']})" for item in st.session_state["quote_items"]
            ])
            # Use the same grading as chat
            from core.demo_spec_grading import grade_quote_response
            grading = grade_quote_response(prompt_summary, str(total))
            # Save to quotes.jsonl
            import json
            from vector_store.quote_embedder import QuoteVectorStore
            quote_entry = {"prompt": prompt_summary, "result": {"items": total_items, "total": total}, "grading": grading}
            quotes_path = Path("data/quotes.jsonl")
            quotes_path.parent.mkdir(parents=True, exist_ok=True)
            with open(quotes_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(quote_entry, ensure_ascii=False) + "\n")
            # Add to vector store
            vs = QuoteVectorStore(data_path=str(quotes_path))
            vs.build_index()

    # --- KB Search UI in sidebar ---
    with st.sidebar:
        st.header("Knowledge Base Search")
        kb_query = st.text_input("Search KB", key="kb_query")
        if kb_query:
            kb_results = search_kb(st.session_state.kb, kb_query)
            if kb_results:
                for title, content in kb_results:
                    st.markdown(f"### {title}")
                    st.markdown(content)
            else:
                st.info("No KB results found.")


    def generate_and_clear():
        prompt = st.session_state.get("prompt_input", "")
        if prompt.strip():
            output = run_quote(prompt.strip())
            data = parse_quote_output(output)
            # --- Spec grading ---
            from core.demo_spec_grading import grade_quote_response
            grading = grade_quote_response(prompt.strip(), output)
            st.session_state.history.append({"prompt": prompt.strip(), "data": data, "grading": grading})
            # --- Store prompt and quote in data/quotes.jsonl and vector store ---
            import json
            from vector_store.quote_embedder import QuoteVectorStore
            quote_entry = {"prompt": prompt.strip(), "result": data, "grading": grading}
            quotes_path = Path("data/quotes.jsonl")
            quotes_path.parent.mkdir(parents=True, exist_ok=True)
            with open(quotes_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(quote_entry, ensure_ascii=False) + "\n")
            # Add to vector store
            vs = QuoteVectorStore(data_path=str(quotes_path))
            vs.build_index()
        # Clear the input after quote generation
        st.session_state["prompt_input"] = ""


    with left:
        st.header("Chat")
        if 'chat_history' not in st.session_state:
            st.session_state['chat_history'] = []

        user_input = st.chat_input('Ask a question or request a quote...')
        if user_input:
            kb_results = search_kb(st.session_state.kb, user_input)
            if kb_results:
                response = kb_results[0][1]
            else:
                # --- Parse and validate chat input against config ---
                # Load config options
                service_options = [k for k in pricing_config.keys() if k != "surcharge"]
                size_options = ["standard", "large"] + [k for k in pricing_config.keys() if k in ["small", "medium", "extra_large"]]
                storey_options = [1, 2, 3]
                surcharge_keys = list(pricing_config.get("surcharge", {}).keys())
                suburb_options = [
                    "None", "Cottesloe", "Subiaco", "Fremantle", "Claremont", "Mosman Park",
                    "Peppermint Grove", "Nedlands", "Dalkeith", "Crawley", "Shenton Park"
                ]
                suburb_map = {
                    "Cottesloe": "travel_cottesloe",
                    "Subiaco": "travel_subiaco",
                    "Fremantle": "travel_fremantle",
                    "Claremont": "travel_claremont",
                    "Mosman Park": "travel_mosman_park",
                    "Peppermint Grove": "travel_peppermint_grove",
                    "Nedlands": "travel_nedlands",
                    "Dalkeith": "travel_dalkeith",
                    "Crawley": "travel_crawley",
                    "Shenton Park": "travel_shenton_park"
                }
                # --- Simple parsing logic (can be replaced with NLP) ---
                import re
                # Try to extract service, qty, size, storey, surcharges, suburb
                service = None
                qty = 1
                size = "standard"
                storey = 1
                selected_surcharges = []
                suburb = "None"
                # Service
                for s in service_options:
                    if re.search(rf"\b{s}\b", user_input, re.IGNORECASE):
                        service = s
                        break
                # Quantity
                qty_match = re.search(r"(\d+)x?", user_input)
                if qty_match:
                    qty = int(qty_match.group(1))
                # Size
                for sz in size_options:
                    if re.search(rf"\b{sz}\b", user_input, re.IGNORECASE):
                        size = sz
                        break
                # Storey
                for st in storey_options:
                    if re.search(rf"\b{st} storey\b|\bstorey {st}\b|\b{st} floor\b|\bfloor {st}\b", user_input, re.IGNORECASE):
                        storey = st
                        break
                # Surcharges
                for sk in surcharge_keys:
                    if re.search(rf"\b{sk}\b", user_input, re.IGNORECASE):
                        selected_surcharges.append(sk)
                # Suburb
                for sub in suburb_options:
                    if re.search(rf"\b{sub}\b", user_input, re.IGNORECASE):
                        suburb = sub
                        break
                if suburb != "None":
                    surcharge_key = suburb_map.get(suburb)
                    if surcharge_key and surcharge_key not in selected_surcharges:
                        selected_surcharges.append(surcharge_key)
                # Validate service
                errors = []
                if not service:
                    errors.append(f"Service type not recognized. Available: {', '.join(service_options)}")
                if size not in size_options:
                    errors.append(f"Size not recognized. Available: {', '.join(size_options)}")
                if storey not in storey_options:
                    errors.append(f"Storey not recognized. Available: {', '.join(map(str, storey_options))}")
                if errors:
                    assistant_msg = "<br>".join(errors)
                else:
                    # Compose scope and run quote
                    scope = {
                        "service": service,
                        "qty": qty,
                        "size": size,
                        "storey": storey,
                        "surcharges": {k: True for k in selected_surcharges}
                    }
                    from logic.pricing_rules import calculate_price
                    result = calculate_price(scope)
                    from core.demo_spec_grading import grade_quote_response
                    grading = grade_quote_response(user_input.strip(), result["total"])
                    score = grading['score']
                    passed = grading['passed']
                    failures = grading['failures']
                    badge_color = 'green' if score == 1.0 else ('orange' if score >= 0.67 else 'red')
                    badge = f"<span style='background-color:{badge_color};color:white;padding:4px 10px;border-radius:8px;font-weight:bold;'>Spec Score: {score}</span>"
                    passed_str = ', '.join(passed) if passed else 'None'
                    failed_str = ', '.join(failures) if failures else 'None'
                    tooltip = "<span title='Passed: {} | Failed: {}'>ℹ️</span>".format(passed_str, failed_str)
                    assistant_msg = f"Quote total: ${result['total']}<br>{badge} {tooltip}<br><b>Passed:</b> {passed_str}<br><b>Failed:</b> {failed_str}"
                st.session_state['chat_history'].append({
                    'user': user_input.strip(),
                    'assistant': assistant_msg
                })
                st.session_state.history.append({"prompt": user_input.strip(), "data": result})

        for exchange in st.session_state['chat_history']:
            st.chat_message('user').write(exchange['user'])
            st.chat_message('assistant').markdown(exchange['assistant'], unsafe_allow_html=True)

        st.subheader("System Resource Usage")
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        st.write(f"CPU Usage: {cpu}%")
        st.write(
            f"Memory Usage: {mem.percent}% ({mem.used // (1024**2)} MB / {mem.total // (1024**2)} MB)"
        )
        try:
            gpus = GPUtil.getGPUs()
            if gpus:
                for gpu in gpus:
                    st.write(
                        f"GPU {gpu.id}: {gpu.name}, Load: {gpu.load*100:.1f}%, Mem: {gpu.memoryUsed}MB/{gpu.memoryTotal}MB"
                    )
            else:
                st.write("No GPU detected.")
        except Exception as e:
            st.write(f"GPU info unavailable: {e}")

        st.subheader("Vector Store Stats")
        try:
            from vector_store.quote_embedder import QuoteVectorStore
            quotes_path = Path("data/quotes.jsonl")
            vs = QuoteVectorStore(data_path=str(quotes_path))
            count = vs.count()
            if count == 0:
                st.warning("Vector store is empty or failed to load. Check if 'data/quotes.jsonl' exists and is populated.")
            else:
                st.write(f"Number of vectors: {count}")
        except Exception as e:
            import traceback
            st.error(f"Could not load vector store: {e}")
            st.code(traceback.format_exc(), language="python")

    with right:
        st.header("Quote")
        if st.session_state.history:
            render_quote(st.session_state.history[-1]["data"])
        else:
            st.write("Enter a job description to generate a quote.")


if __name__ == "__main__":
    main()
