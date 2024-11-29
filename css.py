st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        animation: slide 5s infinite;
    }

    @keyframes slide {
        0% {transform: translateX(0%);}
        50% {transform: translateX(50%);}
        100% {transform: translateX(0%);}
    }
    </style>
    <div class="footer">
        Developed by [Your Name]
    </div>
""", unsafe_allow_html=True)