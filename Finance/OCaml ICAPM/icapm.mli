(**pThe global market type allows to store data concerning the GIM (global international market and the local risk free rate *)
type global_market =
  {
    gim_expected_return: float;
    gim_standard_deviation: float;
    risk_free: float;
  }

(**
The asset_class type stores data concerning a given asset class
*)    
type asset_class =
  {
    country: string;
    asset: string;
    expected_return: float option;
    standard_deviation: float;
    correlation_global: float;
    beta: float option;
    integration_level: float;
    illiquidity_premium: float;
  }


(**
Update the float option values of an asset_class variable 
@param g_market global_market variable
@param asset asset_class variable to update
@return An updated asset_class
 *)
val update_asset_class: global_market -> asset_class -> asset_class

(**
Print an asset_class variable
@param asset_class to print
@return unit
 *)
val print_asset_class: asset_class -> unit
