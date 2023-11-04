def generateHTML(ssid, password, ap, style):
    html = f"""<!DOCTYPE html>
    <html>
        <head> 
            <title>Hackspace Bot</title> 
            <style>
                {style}
            </style>
        </head>
        <body>
            <div>
                <form action="" method="post">
                <table class="controller">
                <tr>
                    <td></td>
                    <td>
                        <button type="submit" formaction="forwards">&#8593</button>
                    </td>
                    <td></td>
                </tr>
                <tr>
                    <td><button type="submit" formaction="left">&#8592</button></td>
                    <td>
                        <button type="submit" formaction="stop">Stop</button>
                    </td>
                    <td>
                        <button type="submit" formaction="right">&#8594</button>
                    </td>
                </tr>
                <tr>
                    <td></td>
                    <td>
                        <button type="submit" formaction="backwards" >&#8595</button>
                    </td>
                    <td></td>
                </tr>
                </table>
            </div>
            """
    html = html + f"""
            <div>
            <table>
                <tr>
                    <td>SSID</td>
                    <td>PASSWORD</td>
                    <td>IP</td>
                </tr>
                <tr>
                    <td>{ssid}</td>
                    <td>{password}</td>
                    <td>{ap.ifconfig()}</td>
                </tr>
            </table>
            </div>
            </form>
    </body>
        </html>
    """
    return html
