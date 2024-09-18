def add_logo_to_map(map_html_path, base64_logo):
    with open(map_html_path, "r") as file:
        map_html = file.read()

    # Inject the logo div at the end of the body tag
    logo_div = f'''
    <div style="
        position: absolute;
        bottom: 20px;
        right: 10px;
        background-color: white;
        padding: 10px;
        border-radius: 8px 8px 0 0;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        z-index: 9999;
    ">
        <img src="data:image/png;base64,{base64_logo}" alt="Logo" style="height: 150px;">
        <p style="margin: 0; font-size: 12px; text-align: center;">© by <a href="https://www.linkedin.com/in/pfennig42/">Pfennig</a> (9/24) at XAMK-Hackathon <br>
        Part of the <a href="https://mapr.mobi/">mapr.mobi</a> project.</p>
    </div>
    '''

    # Insert the logo div before the closing body tag
    updated_map_html = map_html.replace("</body>", logo_div + "</body>")

    # Write the updated HTML back to the file
    with open(map_html_path, "w") as file:
        file.write(updated_map_html)
        
if __name__ == "__main__":
    map = "map_walk_smol"
    with open("logo.txt", "r") as file:
        logo_html = file.read()
    add_logo_to_map(f"{map}.html", logo_html)
    
    