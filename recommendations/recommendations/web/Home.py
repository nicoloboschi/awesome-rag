import uuid

import requests
import streamlit as st

if 'selected_product' not in st.session_state:
    st.session_state.selected_product = None
if "session_id" not in st.session_state:
    st.session_state["session_id"] = uuid.uuid4()


def load_products():
    products = requests.get(f"http://localhost:8002/products?session_id={st.session_state.session_id}").json()
    return products
def display_product_details():
    st.write("")  # Add space
    if st.button("Back Home"):
        st.session_state.selected_product = None
        st.rerun()
        return
    response = requests.get(f"http://localhost:8002/products/{st.session_state.selected_product}?session_id={st.session_state.session_id}").json()
    selected_product = response["selected_product"]
    recommended_products = response["recommended_products"]

    print(selected_product)
    if selected_product:
        st.title(f"Details of {selected_product['name']}")
        st.write(f"**Name:** {selected_product['name']}")
        st.write(f"**Price:** {selected_product['price']}")
        st.write(f"**Description:** {selected_product['description']}")
        st.write("---")
        if recommended_products:
            st.subheader("Recommended Products")
            for product in recommended_products:
                if product['name'] != selected_product['name']:
                    st.write(f"{product['reason']}")
                    if st.button(f"**{product['name']}** - {product['price']}", key="rec" + str(product['id'])):
                        st.session_state.selected_product = product['id']
                        st.rerun()
                        return
                    st.write(product['description'])
                    st.write("---")
    else:
        st.write("Product not found.")


def display_products():
    st.title("List of Products")
    products_and_recs = load_products()
    for product in products_and_recs["products"]:
        col1, col2, col3 = st.columns([1, 2, 4])
        with col1:
            st.write(str(product['id']))
        with col2:
            if st.button(f"**{product['name']}** - {product['price']}", key=product['id']):
                st.session_state.selected_product = product['id']
                st.rerun()
        with col3:
            st.write(product['description'])
        st.write("---")
    st.write("---")
    recommended_products = products_and_recs["recommended_products"]
    if recommended_products:
        st.subheader("Recommended Products")
        for product in recommended_products:
            st.write(f"{product['reason']}")
            if st.button(f"**{product['name']}** - {product['price']}", key="rec" + str(product['id'])):
                st.session_state.selected_product = product['id']
                st.rerun()
                return
            st.write(product['description'])
            st.write("---")

if __name__ == "__main__":
    if 'selected_product' in st.session_state and st.session_state.selected_product:
        display_product_details()
    else:
        display_products()