import gradio as gr
import create_map_poster as cmp
import os

def generate_poster(city, country, theme, distance):
    """
    Gradio wrapper for the poster generation logic.
    """
    try:
        if not city or not country:
            return None, "Error: City and Country are required."
            
        # Load the selected theme into the global variable in create_map_poster
        cmp.THEME = cmp.load_theme(theme)
        
        # Get coordinates for the location
        coords = cmp.get_coordinates(city, country)
        
        # Generate a unique filename
        output_file = cmp.generate_output_filename(city, theme)
        
        # Create the poster
        cmp.create_poster(city, country, coords, int(distance), output_file)
        
        if os.path.exists(output_file):
            return output_file, f"Successfully generated poster for {city}!"
        else:
            return None, "Error: Poster was not saved correctly."
            
    except Exception as e:
        return None, f"Error: {str(e)}"

# Get list of available themes for the dropdown
available_themes = cmp.get_available_themes()
if not available_themes:
    # Fallback if themes dir is empty or not found
    available_themes = ["feature_based"]

# Create Gradio interface
with gr.Blocks(title="City Map Poster Generator", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🏙️ City Map Poster Generator")
    gr.Markdown("Generate beautiful, minimalist map posters for any city in the world using OpenStreetMap data.")
    
    with gr.Row():
        with gr.Column(scale=1):
            city_input = gr.Textbox(label="City", placeholder="e.g. Paris", value="Paris")
            country_input = gr.Textbox(label="Country", placeholder="e.g. France", value="France")
            theme_dropdown = gr.Dropdown(
                choices=available_themes, 
                value=available_themes[0] if available_themes else "feature_based", 
                label="Theme"
            )
            distance_slider = gr.Slider(
                minimum=1000, 
                maximum=50000, 
                step=1000, 
                value=12000, 
                label="Map Radius (meters)"
            )
            generate_btn = gr.Button("🎨 Generate Poster", variant="primary")
            
            status_msg = gr.Markdown("")
            
            gr.Markdown("### 📏 Distance Guide")
            gr.Markdown("""
            - **4,000-6,000m**: Small/dense areas (Venice, Amsterdam center)
            - **8,000-12,000m**: Medium cities (Paris, Barcelona, Manhattan)
            - **15,000-25,000m**: Large metropolitan areas (Tokyo, London, Mumbai)
            """)
        
        with gr.Column(scale=2):
            output_image = gr.Image(label="Generated Poster", type="filepath")

    generate_btn.click(
        fn=generate_poster,
        inputs=[city_input, country_input, theme_dropdown, distance_slider],
        outputs=[output_image, status_msg]
    )
    
    gr.Examples(
        examples=[
            ["Venice", "Italy", "blueprint", 5000],
            ["New York", "USA", "noir", 12000],
            ["Tokyo", "Japan", "japanese_ink", 18000],
            ["San Francisco", "USA", "sunset", 10000],
        ],
        inputs=[city_input, country_input, theme_dropdown, distance_slider]
    )

if __name__ == "__main__":
    # demo.launch()
    # server_name="0.0.0.0" is required for Docker to expose the app
    demo.launch(server_name="0.0.0.0", server_port=7860)
