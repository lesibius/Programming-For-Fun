(**
@author Clementin Castellano
 *)

open Core;;
open Printf;;

(****************************************************************
                        Type Definition
*****************************************************************)
  
(**The global market type allows to store data concerning the GIM (global international market and the local risk free rate *)
type global_market =
  {
    gim_expected_return: float;
    gim_standard_deviation: float;
    risk_free: float;
  }

(**
@The asset_class type stores data concerning a given asset class
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

(****************************************************************
                         Core Functions
*****************************************************************)

    
(*
Generic function to compute the Sharpe ratio
 *)
let sharpe_ratio expected_return rf st_dev =
  let excess_return = expected_return -. rf in
  excess_return /. st_dev

(*
Implementation of the generic Sharpe ratio function for global_market variables
 *)
let gim_sharpe_ratio =
  fun {risk_free; gim_expected_return; gim_standard_deviation} ->
  sharpe_ratio gim_expected_return risk_free gim_standard_deviation

(*
Implementation of the generic Sharpe ratio function for asset_class variables
 *)
let asset_sharpe_ratio asset rf =
  match asset.expected_return with
  | None -> None
  | Some exp_return ->
     Some (sharpe_ratio exp_return rf asset.standard_deviation)

(**
Update the float option values of an asset_class variable 
@param g_market global_market variable
@param asset asset_class variable to update
@return An updated asset_class
 *)          
let update_asset_class g_market asset =
  let sharpe_gim = gim_sharpe_ratio g_market in
  let rho = asset.correlation_global in
  let sigma = asset.standard_deviation in
  let integration_level = asset.integration_level in
  let illiquidity_premium = asset.illiquidity_premium in
  let premium = sigma *. sharpe_gim *. (1.0 +. integration_level *. (rho -. 1.0)) +. illiquidity_premium in
  let exp_return = g_market.risk_free +. premium in
  let asset_beta = sigma *. rho /. g_market.gim_standard_deviation in
  {asset with expected_return = Some exp_return; beta = Some asset_beta}


(****************************************************************
                            Print Utils
*****************************************************************)

(*Print a line of '%' char*)    
let print_main_line () = print_string ((String.make 50 '%') ^ "\n")

(*Print a line of '-' char*)
let print_sep_line () = print_string ((String.make 50 '-') ^ "\n")
                                     
(*Util for generic printing*)
type data_val =
  | Float of float
  | Str of string

(*Print a line with:
- desc = right justified description of the field
- value = left justified value
- percent = bool (true to add percent to a Float data)*)             
let print_line desc value percent=
  let str_val =
    match value with
    | Float fval ->
       let raw_val = sprintf "%0.*f" 2 fval in
       if percent then
         raw_val ^ "%"
       else raw_val
    | Str sval ->
       sval in
  let remaining_length = 50 - String.length desc - String.length str_val in
  print_string (desc ^ (String.make remaining_length ' ') ^ str_val);
  print_newline ()
      

(**
Print an asset_class variable
@param asset_class to print
@return unit
 *)                                     
let print_asset_class = fun
    { country; asset; expected_return; standard_deviation; correlation_global; beta; integration_level; illiquidity_premium} ->
  let print_header () =
    print_line "Country:" (Str country) false;
    print_line "Asset:" (Str asset) false in
  let print_return_characteristics () =
    begin
      match expected_return with
      | Some e -> print_line "Expected return:" (Float (100.0 *. e)) true
      | None -> print_line "Expected return: " (Str "Unknown") false
    end;
    print_line "Standard deviation:" (Float (100.0 *. standard_deviation)) true;
    print_line "Illiquidity premium:" (Float (100.0 *. illiquidity_premium)) true in
  let print_market_related () =
    print_line "Integration level:" (Float (100.0 *. integration_level)) true;
    print_line "Correlation with the GIM:" (Float (100.0 *. correlation_global)) false;
    begin
      match beta with
      | None -> print_line "GIM Beta" (Str "Unknown") false
      | Some b -> print_line "GIM Beta" (Float b) false
    end in
  print_main_line ();
  print_header ();
  print_sep_line ();
  print_return_characteristics ();
  print_sep_line ();
  print_market_related ();
  print_main_line();
  print_string "\n";
