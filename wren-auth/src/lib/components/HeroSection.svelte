<script lang="ts">
  import { AuthForm } from "$components";
  import heroImage from "$assets/gradient.svg";
</script>

<section class={`flex flex-col h-screen sm:px-14`}>
  <div class="absolute inset-0 z-[-1]">
    <img src={heroImage} alt="" class="w-full h-100 object-cover" />
  </div>
  <div
    class="flex flex-col sm:flex-row w-full h-full items-center justify-between"
  >
    <div class="hidden lg:flex lg:flex-col lg:w-9/20">
      <h1 class="text-dark-blue font-bold text-5xl mb-6">
        Intelligent, Efficient and <br />Productive
      </h1>
      <h2 class="text-dark-blue font-medium text-2xl">
        An AI Applications Hub
      </h2>
    </div>
    <div class="lg:w-9/20 lg:h-3/4 bg-neutre">
      <AuthForm />
    </div>
  </div>
  <div
    class="flex w-full justify-center gap-10 fixed bottom-0 mb-10 sm:justify-start"
  >
    <a class="text-primary font-bold text-xs" href="mailto:contato@s-c.ai"
      >Contact Us</a
    >
    <a class="text-primary font-bold text-xs" href="https://s-c.ai"
      >Our website</a
    >
  </div>
</section>
