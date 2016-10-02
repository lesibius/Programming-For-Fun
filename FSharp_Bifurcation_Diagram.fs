(**********************************************************************************************
                    Plotting the Logistic Equation Bifurcation Diagram
**********************************************************************************************)

(*
Lastly, I got interested in the Chaos Theory and I wanted to create my own program to plot
bifurcation diagrams. 

I thought it would be a good idea to do it on F# as it would allow to conveniently use the
iterated function definition as an input.

The program works as expected, except that it is very slow. I suspect two reasons for this:
1) I used a recursive loop to generate the points
2) I am using sequences, which I have to admit, I do not yet fully understand when they are
    a good idea to use. I think the program is actually computing the path of the iterated
    function from scratch each time a new point is calculated.

As usual, the beauty of F# is at work, and the number of lines to create the full program 
is fairly low.

*)




open System
open FSharp.Charting
open System.Drawing

let logisticequation r = fun x0 ->
    r * x0 * (1.0 - x0)
    
let generatesequence x0 = fun func -> 
    Seq.unfold (fun x -> Some (x, func x)) x0

let shortensequence notshowed showed = fun (sequence:seq<float>) ->
    sequence |> Seq.skip notshowed |> Seq.take showed

let attributexvalue r = fun (sequence:seq<float>) -> 
    Seq.map (fun x -> (r,x)) sequence

let concatenatedsequence shortener rmin rmax nr x0 = fun func ->
    let deltar = (rmax - rmin)/(float nr)
    let rec loop currentseq r n =
        match n with
        | N when N > nr -> currentseq
        | _ -> loop (func r |> (generatesequence x0) |> shortener |> attributexvalue r |> Seq.append currentseq) (r + deltar) (n + 1)
    loop (Seq.empty) rmin 0



let printmulti funtoprint x0 maxStep =
    let rec loop value step =
        match step with
        |   n when n >= maxStep -> ()
        |   _ ->
            let tempvalue = (funtoprint value) 
            printfn "%A" tempvalue
            loop tempvalue (step + 1)
    loop x0 1
    


(*****************************************************************************
                            Parameters
*****************************************************************************)

let rmin = 0.0
let rmax = 4.0
let npointsnotdisplayed = 1000
let npointsdisplayed = 100
let numberofrvalue = 100
let startingvalue = 0.2


(*****************************************************************************
                            Main Code
*****************************************************************************)

[<EntryPoint>]
let main argv = 
    
    let seqtodisplay = (concatenatedsequence (shortensequence npointsnotdisplayed npointsdisplayed) rmin rmax numberofrvalue startingvalue logisticequation) |> Seq.toArray

    seqtodisplay |> Chart.Point |> Chart.Show
    

    //printfn "%A" (logisticequationSeq 4.0 0.2)
    0 // retourne du code de sortie entier
