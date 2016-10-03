(**********************************************************************************************

                    Plotting the Logistic Equation Bifurcation Diagram

**********************************************************************************************)

(*
Lastly, I got interested in the Chaos Theory and I wanted to create my own program to plot
bifurcation diagrams. 

I thought it would be a good idea to do it on F# as it would allow to conveniently use the
iterated function definition as an input.

This program use both sequences and arrays to function. The advantage of sequences is that
they allow to create an infinite "list", while arrays offer a faster speed of execution.

In order to accelerate the plotting, I used the RProvider library to create the chart.
The first implementation of this code used FSharp.Charting, which was really slow.

*)

(*****************************************************************************
                            Loading Libraries
*****************************************************************************)

open RDotNet
open RProvider
open RProvider.graphics

//These two libraries allow to export the path as CSV
open System.IO
open System.Diagnostics


(*****************************************************************************
                            Equations for Bifurcation
*****************************************************************************)


let logisticequation r = fun x0 ->
    r * x0 * (1.0 - x0)

let cubicequation r = fun x0 ->
    r * (x0 ** 2.0) * ( 1.0 - x0)

let sinefunction r = fun x0 ->
    r * sin((System.Math.PI * x0)/2.0)

//To add other equations, define a new function with the following form:
// <float> -> (<float> -> <float>)
// The parameter (r:float) is the one that is varied to create the diagram
    
(****************************************************************************
                            Generating Points
*****************************************************************************)

//Generate an infinite sequence using the equation provided
let generatesequence x0 = fun func -> 
    Seq.unfold (fun x -> Some (x, func x)) x0

//Shorten the sequence so the first iteration are not displayed
let shortensequence notshowed showed = fun (iteratedValues:seq<float>) ->
    iteratedValues |> Seq.skip notshowed |> Seq.take showed |> Seq.toArray

//Remove the values that are outside the plot on the y axis
let removeupanddown xmin xmax = fun (iteratedValues:float []) ->
    iteratedValues |> Array.filter (fun x -> (x >= xmin) && (x <= xmax))

//In order to speed the plotting process, unnecessary values (i.e. periodic values) are removed
let removeperiodicvalue = fun (iteratedValues:float []) ->
    match iteratedValues |> Array.isEmpty with
    | true -> None
    | false -> 
        let firstValue = iteratedValues |> Array.item 0
        let x =  Array.sub iteratedValues 1 ((iteratedValues |> Array.length) - 1) |>Array.tryFindIndex (fun x -> x = firstValue)
        match x with 
        | Some index -> Some (Array.sub iteratedValues 0 (index + 1))
        | None -> Some(iteratedValues)

//This function has the following form: <float []> -> <option <float * float []>
//It creates the coordinates of the points to plot for a single value of the function parameter
let attributexvalue r = fun (sequence:float [] option) -> 
    match sequence with
    | Some value -> Some (Array.map (fun x -> (r,x)) value)
    | None -> None
    
//Create the points through a recursive loop
let concatenatedsequence shortener rmin rmax nr x0 xmin xmax = fun func ->
    let deltar = (rmax - rmin)/(float nr)
    let rec loop currentArray r n =
        match n with
        | N when N > nr -> currentArray
        | _ -> 
            let tempSeq = func r |> (generatesequence x0) |> shortener |> (removeupanddown xmin xmax) |> removeperiodicvalue |> attributexvalue r 
            let tempArray =
                match tempSeq with
                | Some value -> value |> Array.append currentArray
                | None -> currentArray
            loop tempArray (r + deltar) (n + 1)
    loop (Array.empty) rmin 0


(*****************************************************************************
                            Charting Points
*****************************************************************************)
//All this is done through R



(*****************************************************************************
                            Exporting as CSV
*****************************************************************************)

let exportArrayAsCsv (values: (float*float) []) =
    use wr = StreamWriter(@"mypath.csv", true)
    let arraytoprint = Array.map (fun (r,x) -> sprintf "%f,%f" r x) values
    arraytoprint |> Array.map (fun x -> wr.WriteLine(x))
    
    

     

(*****************************************************************************
                            Parameters
*****************************************************************************)
//NB: with these settings, the plot is zommed ~ x100
let rmin = 3.56
let rmax = 3.58
let xmin = 0.45
let xmax = 0.54
let npointsnotdisplayed = 1000
let npointsdisplayed = 500
let numberofrvalue = 1000
let startingvalue = 0.2


(*****************************************************************************
                            Main Code
*****************************************************************************)

[<EntryPoint>]
let main argv = 
    //Creates the "shortener" to remove points before the attraction actually occurs
    let shortener = shortensequence npointsnotdisplayed npointsdisplayed

    //Create
    let pointstodisplay = (concatenatedsequence shortener rmin rmax numberofrvalue startingvalue xmin xmax logisticequation)

    //Uncomment to see some iterations
    //printfn "%A" seqtodisplay

    
    let x = pointstodisplay |> Array.map (fun (x,y) -> x) 
    let y = pointstodisplay |> Array.map (fun (x,y) -> y) 
    
    R.plot(namedParams [   
        "x", box x;
        "y", box y; 
        "pch", box 19;
        "cex",box 0.1;
        "type", box "p"; 
        "col", box "lightgrey";
        "ylim", box [xmin; xmax] ])

    0 // retourne du code de sortie entier
