open Core;;
open Icapm;;
open Icapm_allocation;;


(* Inputs of the model: global market and asset classes characteristics*)
  
let gm =
  let risk_free = 0.03 in
  let gim_expected_return = 0.03 +. 0.28 *. 0.07 in
  let gim_standard_deviation = 0.07 in
  {risk_free; gim_expected_return; gim_standard_deviation}
  
let us_equities =
  {
    country = "US";
    asset = "Equities";
    expected_return = None;
    standard_deviation = 0.157;
    correlation_global = 0.85;
    beta = None;
    integration_level = 0.8;
    illiquidity_premium = 0.0;
  }

    let us_fixed_income =
  {
    country = "US";
    asset = "Fixed income";
    expected_return = None;
    standard_deviation = 0.038;
    correlation_global = 0.75;
    beta = None;
    integration_level = 0.8;
    illiquidity_premium = 0.0;
  }
    
let world_equities =
  {
    country = "Non-US";
    asset = "Equities";
    expected_return = None;
    standard_deviation = 0.156;
    correlation_global = 0.80;
    beta = None;
    integration_level = 0.8;
    illiquidity_premium = 0.0;
  }


let world_fixed_income =
  {
    country = "Non-US";
    asset = "Fixed income";
    expected_return = None;
    standard_deviation = 0.091;
    correlation_global = 0.7;
    beta = None;
    integration_level = 0.8;
    illiquidity_premium = 0.0;
  }

let us_real_estate =
  {
    country = "US";
    asset = "Real estate";
    expected_return = None;
    standard_deviation = 0.115;
    correlation_global = 0.5;
    beta = None;
    integration_level = 0.7;
    illiquidity_premium = 0.003;
  }



(*Bind asset classes and compute missing characteristics*)
let asset_list = [us_equities;us_fixed_income;world_equities;world_fixed_income;us_real_estate]

let updated_list = List.map (update_asset_class gm) asset_list

(*Optimized portfolios*)
let max_ret_p =  maximize_return updated_list gm 0.12 (Some (Array.make 5 (0.0))) (Some (Array.make 5 0.35))
let max_ret_p_description = "This portfolio intends to maximize the expected return, while keeping the volatility below a given threshold (12%). Short-selling is prohibited and no asset can be above a 35% holding threshold"    

let min_vol_p = minimize_vol updated_list gm 0.07 (Some (Array.make 5 (-. 0.10))) None
let min_vol_p_description = "This portfolio intends to minimize the volatility, while keeping the return above a certain threshold (7%). Short-selling cannot exceed 10% for a given asset class"

(*Print results*)
                              
let () =
  List.iter print_asset_class updated_list;
  print_portfolio max_ret_p gm max_ret_p_description;
  print_portfolio min_vol_p gm min_vol_p_description
  

    
