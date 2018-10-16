using System.Collections;
using System.Collections.Generic;
using Mapbox.Unity.Location;
using Mapbox.Unity.Map;
using UnityEngine;

public class spawnTarget : MonoBehaviour {

    [SerializeField]
    public AbstractMap mapManager;

    public GameObject player;
    public gpsData currGPS;
    private int idx = 0;

    // Use this for initialization
    void Start () {
		if (mapManager == null)
        {
            Debug.Log("Did you forget to add the map?");
        }
        else
        {
            

        }
	}
    private void OnEnable()
    {
       
        
    }

    // Update is called once per frame
    void Update () {
        
        currGPS = this.GetComponent<dataController>().getGPS(idx++);
        
        Vector3 pos = mapManager.GeoToWorldPosition(new Mapbox.Utils.Vector2d(double.Parse(currGPS.Latitude), double.Parse(currGPS.Longitude)));
        pos.y += player.GetComponent<Renderer>().bounds.size.y / 2;// +float.Parse(currGPS.Elevation);
        player.transform.position = pos;
    }
}
