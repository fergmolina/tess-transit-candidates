"""Fetch ASAS-SN Sky Patrol v2 light curve (V and g) for TIC 89247735 and save as CSV."""
from pyasassn.client import SkyPatrolClient
import pandas as pd, numpy as np
def main():
    c=SkyPatrolClient()
    ra,dec=275.22345,-45.56164
    q=c.cone_search(ra_deg=ra,dec_deg=dec,radius=0.01)
    print('cone search targets:'); print(q)
    res=c.cone_search(ra_deg=ra,dec_deg=dec,radius=0.01,download=True,threads=1)
    df=res.data
    print(df.head()); print(df.columns.tolist(), len(df))
    df.to_csv('/Users/fernando/Desktop/NASA/results/external_review/data/asassn/asassn_89247735_raw.csv',index=False)
if __name__=='__main__': main()
