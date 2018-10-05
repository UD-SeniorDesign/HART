using System.Collections;
using System.Collections.Generic;
using Mapbox.Unity.Location;
using Mapbox.Unity.Map;
using UnityEngine;

public class spawnTarget : MonoBehaviour {

    [SerializeField]
    public AbstractMap mapManager;

    public GameObject player;

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
        Vector3 pos = mapManager.GeoToWorldPosition(new Mapbox.Utils.Vector2d(39.6677478093179f, -75.7518574609092f));
        //Debug.Log(pos);
        pos.y += player.GetComponent<Renderer>().bounds.size.y/2;
        player.transform.position = pos;
    }
}
