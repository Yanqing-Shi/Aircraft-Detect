import pandas as pd
from opensky_api import OpenSkyApi


class airport_activity():
    def __init__(self,airport:str,api)->None:
        self.airportcode=airport
        self.api=api
        log=[]
        self.log=log
        
    def find_coordinate(self,list):
        lat=list.loc[list['ident']==self.airportcode,'latitude_deg'].values
        lon=list.loc[list['ident']==self.airportcode,'longitude_deg'].values
        #1 deg=54.6mi in long and 69mi in lat
        minlon=lon-0.1
        maxlon=lon+0.1
        minlat=lat-0.07
        maxlat=lat+0.07
        return minlat,maxlat,minlon,maxlon
    
    def get_current_state(self,minlat,maxlat,minlon,maxlon):
        states = self.api.get_states(bbox=(minlat,maxlat,minlon,maxlon))
        statelist=[]
        for i in states.states:
            if i.geo_altitude==None or i.geo_altitude<1000:
                statelist.append(i)

        
        return statelist
    def make_list(self,frame):
        icao=frame[0]
        callsign=frame[1]
        on_ground=frame[8]
        st=[]
        df = pd.DataFrame({
        'callsign': callsign,
        'icao': icao,
        'ground': on_ground,
        'status': st # 0 fornot in the range 
        })
        df_sorted = df.sort_values(by='icao')

        return df_sorted
    
    def update_list(self,new):
        newcopy=new
        for i in range(0,len(new)):
            flag=0
            for j in range(0,len(self.log)):
                if new.loc[i, 'icao']==self.log.loc[j,'icao']:
                    flag=1
                    break
            if flag==0:
                self.log.append([new.loc[j, 'callsign'],new.loc[j, 'icao'],new.loc[j, 'ground'],1])

        for i in range(0,len(self.log)):
            flag=0
            for j in range(0,len(new)):
                if new.loc[j, 'icao']==self.log.loc[i,'icao']:
                    flag=1
                    break
            if flag==0:
                self.log.remove(self.log[i])
        print(self.log)




