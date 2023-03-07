import cherrypy
import os
# import json

class FormHandler(object):
    @cherrypy.expose
    def index(self):
        return '''
            <html>
            <body>
            <h1>Sensor Configuration</h1>
            <form method="post" action="submit">
              
              <label for="Location">Location:</label>
              <input type="text" name="Location"><br>
              <label for="Threshold">Threshold:</label>
              <input type="text" name="Threshold"><br>
              
              <label for="Sensor">Select:</label>
                <select name="Sensor">
                    <option value="AHT20">AHT20</option>
                    <option value="W1ThermSensor">RTD</option>
                    <option value="K-Type">k-Type</option>
                    <option value="MLX90614_temp">NIR</option>
                </select>

            <input type="submit" value="Submit">
            </form>
            </body>
            </html>
        '''

    @cherrypy.expose
    def submit(self, Location=None, Threshold=None, Sensor=None):
        if Location and Threshold and Sensor:
            with open(cherrypy.config.get('data_file_path', 'app/config.txt'), 'w') as f:
                # f.write(f"Location:{Location},Threshold:{Threshold},Sensor:{Sensor}\n")
                # loc=f"{Location}"
                data={'Location':f"{Location}",'Threshold':f"{Threshold}",'Sensor':f"{Sensor}"}
                print(data)
                f.write(str(data))
                # json_data=json.dumps(list(data))
                # f.write(json_data)
                
            return f"Configuration set is now to {Sensor} with Threshold {Threshold} at {Location}!"
        else:
            return "Please select params."

if __name__ == '__main__':
    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', '8080')),
        # 'DATA_FILE': os.environ.get('DATA_FILE', '/app/data.txt')
    })
    cherrypy.quickstart(FormHandler())

