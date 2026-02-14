def load_login_background():
    return """
    <style>

    /* Dark Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        background-size: 400% 400%;
        animation: gradientMove 15s ease infinite;
    }

    @keyframes gradientMove {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Animated Stock Line */
    .graph-line {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 200px;
        overflow: hidden;
        z-index: 0;
    }

    .graph-line svg {
        width: 200%;
        height: 100%;
        animation: slideGraph 10s linear infinite;
    }

    @keyframes slideGraph {
        from {transform: translateX(0);}
        to {transform: translateX(-50%);}
    }

    /* Login Card */
    .login-box {
        background: rgba(0, 0, 0, 0.8);
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0px 0px 25px rgba(0, 255, 255, 0.3);
        backdrop-filter: blur(10px);
        z-index: 2;
        position: relative;
    }

    </style>

    <div class="graph-line">
        <svg viewBox="0 0 1000 200" preserveAspectRatio="none">
            <polyline 
                fill="none" 
                stroke="#00ffcc" 
                stroke-width="3"
                points="
                0,150 
                100,120 
                200,140 
                300,90 
                400,110 
                500,70 
                600,100 
                700,60 
                800,80 
                900,40 
                1000,70
                " />
        </svg>
    </div>
    """