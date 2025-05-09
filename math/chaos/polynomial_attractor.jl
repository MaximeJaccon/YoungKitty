
using GLMakie
using ProgressBars
using Random

Polynomial((x, y), a_0, a_1, a_2, a_3, a_4, a_5, a_6, a_7, a_8, a_9, a_10, a_11) = Point2f(a_0 + a_1*x + a_2*x^2 + a_3*x*y + a_4*y + a_5*y^2, a_6 + a_7*x + a_8*x^2 + a_9*x*y + a_10*y + a_11*y^2)

function trajectory(fn, x0, y0, kargs...; n=1000)
    xy = zeros(Point2f, n + 1)
    xy[1] = Point2f(x0, y0)
    @inbounds for i in 1:n
        xy[i+1] = fn(xy[i], kargs...)
    end
    return xy
end

function attractor_code(code::String)
    conversion_dict = Dict(
        "A" => -1.2, "B" => -1.1, "C" => -1.0, "D" => -0.9,
        "E" => -0.8, "F" => -0.7, "G" => -0.6, "H" => -0.5,
        "I" => -0.4, "J" => -0.3, "K" => -0.2, "L" => -0.1,
        "M" => 0.0, "N" => 0.1, "O" => 0.2, "P" => 0.3, 
        "Q" => 0.4, "R" => 0.5, "S" => 0.6, "T" => 0.7,
        "U" => 0.8, "V" => 0.9, "W" => 1.0, "X" => 1.1,
        "Y" => 1.2
    )
    values = [0.0, 0.0]
    for character in split(code, "")
        val = conversion_dict[character]
        push!(values, val)
    end
    return values
end

#=
cargs = [attractor_code("GLXOESFTTPSV"),
    attractor_code("MCRBIPOPHTBN"),
    attractor_code("VBWNBDELYHUL"),
    attractor_code("FIRCDERRPVLD"),
    attractor_code("QFFVSLMJJCCR"),
    attractor_code("LUFBBFISGJYS"),
    attractor_code("EJYDREGLYQPV"),
    attractor_code("HIYIWHOKNVCG"),
    attractor_code("MSSSRRPADDSO"),
    attractor_code("OIHVGHAHGYRK"),
    attractor_code("RALLTIOBDULT"),
    attractor_code("WJJFXGXHTRPG")
]
=#

fig = Figure(size=(1500, 1500))
ax = Axis(fig[1, 1]; backgroundcolor = RGBAf(0, 0, 0, 1))
cmap = to_colormap(:BuPu_9)
cmap[1] = RGBAf(1, 1, 1, 1) 


n_points = 10^6
cargs = [attractor_code("CVQKGHQTPHTE")]
print(cargs)

points = trajectory(Polynomial, 0, 0,0.8, 1.0, -1.2, -1.0, 1.1, -0.9, 0.4, -0.4, -0.6, -0.2, -0.5, -0.7; n=n_points)
x_coords = [p[1] for p in points]
y_coords = [p[2] for p in points]

index = 1:n_points
frames= 1:2000

record(fig, "polynomial_attractor_6.mp4", frames; framerate = 100) do i
    stop = i * 500
    start = stop - 499
    range = start:stop
    scatter!(
        ax, x_coords[range], y_coords[range], markersize=0.001, color=RGBAf(1, 1, 1, 1)
    )
end
